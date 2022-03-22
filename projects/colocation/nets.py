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
from modules.ensembles import QEnsembleInputs, QEnsembleHead
from modules.vision import AtariVisionTorso
from modules.usfa import ConcatFlatStatePolicy

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

def embed_task(inputs, task_embedder):
  #literally just grab the task vector
  task = inputs.observation.task
  return task_embedder(task).astype(jnp.int32)

def prediction_prep_fn(inputs, memory_out, task_embedder, **kwargs):
  """
  Concat task with memory output.
  """
  task = embed_task(inputs, task_embedder)
  return jnp.concatenate((memory_out, task), axis=-1)

# ======================================================
# Networks
# ======================================================

def r2d1(config, env_spec):
  num_actions = env_spec.actions.num_values

  return BasicRecurrent(
    inputs_prep_fn=convert_floats,
    vision_prep_fn=get_image_from_inputs,
    vision=AtariVisionTorso(flatten=True),
    memory_prep_fn=OAREmbedding(num_actions=num_actions),
    memory=hk.LSTM(config.memory_size),
    prediction_prep_fn=functools.partial(prediction_prep_fn,
      task_embedder=lambda x: x #stupid simple task embedder lol
      ),
    prediction=DuellingMLP(num_actions, hidden_sizes=[config.out_hidden_size])
  )