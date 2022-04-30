"""Modules for computing custom embeddings."""

import dataclasses

from acme.jax.networks import base
from acme.wrappers import observation_action_reward
import haiku as hk
import jax
import jax.numpy as jnp
import numpy as np
Images = jnp.ndarray



class OAREmbedding(hk.Module):
  """Module for embedding (observation, action, reward, task) inputs together."""

  def __init__(self, num_actions, concat=True, observation=True, **kwargs):
    super(OAREmbedding, self).__init__()
    self.num_actions = num_actions
    self.concat = concat
    self.observation = observation

  def __call__(self,
    inputs: observation_action_reward.OAR, obs: jnp.array=None) -> jnp.ndarray:
    """Embed each of the (observation, action, reward) inputs & concatenate."""

    # Do a one-hot embedding of the actions.
    action = jax.nn.one_hot(
        inputs.action, num_classes=self.num_actions)  # [T?, B, A]

    # Map rewards -> [-1, 1].
    reward = jnp.tanh(inputs.reward)

    # Add dummy trailing dimensions to rewards if necessary.
    while reward.ndim < action.ndim:
      reward = jnp.expand_dims(reward, axis=-1)

    # Concatenate on final dimension.
    items = [action, reward]

    if self.observation:
      assert obs is not None, "provide observation"
      items.append(obs)

    if self.concat:
      items = jnp.concatenate(items, axis=-1)  # [T?, B, D+A+1]

    return items


class OneHotTask(hk.Module):
  """docstring for OneHotTask"""
  def __init__(self, size, dim, **kwargs):
    super(OneHotTask, self).__init__()
    self.size = size
    self.dim = dim
    self.embedder = hk.Embed(vocab_size=size, embed_dim=dim, **kwargs)
  
  def __call__(self, khot):

    each = self.embedder(jnp.arange(self.size))
    weighted = each*jnp.expand_dims(khot, axis=1)
    return weighted.sum(0)

  @property
  def out_dim(self):
    return self.dim


class Identity(hk.Module):
  """docstring for OneHotTask"""
  def __init__(self, dim):
    super(Identity, self).__init__()
    self.dim = dim
  
  def __call__(self, x):
    return x

  @property
  def out_dim(self):
    return self.dim

class LanguageTaskEmbedder(hk.Module):
  """Module that embed words and then runs them through GRU."""
  def __init__(self, vocab_size, word_dim, sentence_dim, task_dim=None, initializer='TruncatedNormal', compress='last', **kwargs):
    super(LanguageTaskEmbedder, self).__init__()
    self.vocab_size = vocab_size
    self.word_dim = word_dim
    self.compress = compress
    initializer = getattr(hk.initializers, initializer)()
    self.embedder = hk.Embed(
      vocab_size=vocab_size,
      embed_dim=word_dim,
      w_init=initializer,
      **kwargs)
    self.sentence_dim = sentence_dim
    self.language_model = hk.GRU(sentence_dim)

    if task_dim is None or task_dim is 0:
      self.task_dim = sentence_dim
      self.task_projection = lambda x:x
    else:
      self.task_dim = task_dim
      self.task_projection = hk.Linear(task_dim)
  
  def __call__(self, x : jnp.ndarray):
    """Embed words, then run through GRU.
    
    Args:
        x (TYPE): B x N
    
    Returns:
        TYPE: Description
    """
    B, N = x.shape
    initial = self.language_model.initial_state(B)
    words = self.embedder(x) # B x N x D
    words = jnp.transpose(words, (1,0,2))  # N x B x D
    sentence, _ = hk.static_unroll(self.language_model, words, initial)
    if self.compress == "last":
      task = sentence[-1] # embedding at end
    elif self.compress == "sum":
      task = sentence.sum(0)
    else:
      raise NotImplementedError(self.compress)

    task = self.task_projection(task)
    return task


  @property
  def out_dim(self):
    return self.task_dim
