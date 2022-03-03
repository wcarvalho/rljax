from typing import Callable, Optional, Tuple, NamedTuple
import functools

from acme.jax.networks import duelling
from acme.jax import networks as networks_lib
from acme.wrappers import observation_action_reward

import dataclasses
import haiku as hk
import jax
import jax.numpy as jnp

from agents import td_agent
from agents.td_agent.types import Predictions
from modules.basic_archs import BasicRecurrent
from modules.embedding import OAREmbedding, LanguageTaskEmbedder
from modules import farm
from modules.farm_model import FarmModel, FarmCumulants
from modules.vision import AtariVisionTorso

from utils import data as data_utils

class DuellingMLP(duelling.DuellingMLP):
  def __call__(self, *args, **kwargs):
    kwargs.pop("key", None)
    q = super().__call__(*args, **kwargs)
    return Predictions(q=q)

# ======================================================
# Processing functions
# ======================================================

def convert_floats(inputs):
  return jax.tree_map(lambda x: x.astype(jnp.float32), inputs)

def get_image_from_inputs(inputs : observation_action_reward.OAR):
  return inputs.observation.image/255.0

def make_farm_prep_fn(num_actions):
  """
  Return farm inputs, (1) obs features (2) [action, reward] vector
  """
  embedder = OAREmbedding(
    num_actions=num_actions,
    observation=False)
  def prep(inputs, obs):
    return farm.FarmInputs(
      image=obs, vector=embedder(inputs))

  return prep

def flatten_structured_memory(memory_out, **kwargs):
  return memory_out.reshape(*memory_out.shape[:-2], -1)

def prep_task(inputs, task_embedder):
  """Convert task to ints, batchapply if necessary, and run through embedding function."""
  task = inputs.observation.task
  has_time = len(task.shape) == 3
  batchfn = hk.BatchApply if has_time else lambda x:x
  return batchfn(task_embedder)(task.astype(jnp.int32))

# ======================================================
# R2D1
# ======================================================

def prediction_prep_fn(inputs, memory_out, task_embedder, **kwargs):
  """
  Concat task with memory output.
  """
  task = prep_task(inputs, task_embedder)
  return jnp.concatenate((memory_out, task), axis=-1)

def farm_prediction_prep_fn(inputs, memory_out, task_embedder, **kwargs):
  """
  Concat task with memory output.
  """
  task = prep_task(inputs, task_embedder)
  return jnp.concatenate((flatten_structured_memory(memory_out), task), axis=-1)

def r2d1(config, env_spec):
  num_actions = env_spec.actions.num_values

  return BasicRecurrent(
    inputs_prep_fn=convert_floats,
    vision_prep_fn=get_image_from_inputs,
    vision=AtariVisionTorso(flatten=True),
    memory_prep_fn=OAREmbedding(num_actions=num_actions),
    memory=hk.LSTM(config.memory_size),
    prediction_prep_fn=functools.partial(prediction_prep_fn,
      task_embedder=LanguageTaskEmbedder(
        vocab_size=config.max_vocab_size,
        word_dim=config.word_dim,
        task_dim=config.word_dim),
      ),
    prediction=DuellingMLP(num_actions, hidden_sizes=[config.out_hidden_size])
  )

def r2d1_farm(config, env_spec):
  num_actions = env_spec.actions.num_values

  return BasicRecurrent(
    inputs_prep_fn=convert_floats,
    vision_prep_fn=get_image_from_inputs,
    vision=AtariVisionTorso(flatten=False),
    memory_prep_fn=make_farm_prep_fn(num_actions),
    memory=farm.FARM(config.module_size, config.nmodules),
    prediction_prep_fn=functools.partial(farm_prediction_prep_fn,
      task_embedder=LanguageTaskEmbedder(
        vocab_size=config.max_vocab_size,
        word_dim=config.word_dim,
        task_dim=config.word_dim),
      ),
    prediction=DuellingMLP(num_actions, hidden_sizes=[config.out_hidden_size])
  )

def r2d1_farm_model(config, env_spec):
  num_actions = env_spec.actions.num_values

  return BasicRecurrent(
    inputs_prep_fn=convert_floats,
    vision_prep_fn=get_image_from_inputs,
    vision=AtariVisionTorso(flatten=False),
    memory_prep_fn=make_farm_prep_fn(num_actions),
    memory=farm.FarmSharedOutput(
      module_size=config.module_size,
      nmodules=config.nmodules,
      out_layers=config.out_layers),
    prediction_prep_fn=functools.partial(farm_prediction_prep_fn,
      task_embedder=LanguageTaskEmbedder(
        vocab_size=config.max_vocab_size,
        word_dim=config.word_dim,
        task_dim=config.word_dim),
      ),
    prediction=DuellingMLP(num_actions, hidden_sizes=[config.out_hidden_size]),
    aux_tasks=FarmModel(
      config.model_layers*[config.module_size],
      num_actions=num_actions,
      activation=getattr(jax.nn, config.activation)),
  )