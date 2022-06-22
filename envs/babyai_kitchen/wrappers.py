import gym
import numpy as np

class MissionIntegerWrapper(gym.core.ObservationWrapper):
  """
  Wrapper to convert mission to integers.
  """

  def __init__(self, env, instr_preproc, struct_and=False, max_length=30):
    super().__init__(env)

    self.instr_preproc = instr_preproc
    self.max_length = max_length
    self.struct_and = struct_and

    if self.struct_and:
      shape = (self.max_length, self.max_length)
    else:
      shape = (1, self.max_length,)

    self.observation_space.spaces['mission'] = gym.spaces.Box(
        low=0,
        high=1,
        shape=shape,
        dtype='uint8'
    )

  def observation(self, obs):
    mission = self.instr_preproc(obs['mission'])
    assert len(mission) <= self.max_length

    if self.struct_and:
      and_token = self.instr_preproc.vocab['and']
      idx = np.where(mission != and_token)[0]
      split = np.split(mission[idx],np.where(np.diff(idx)!=1)[0]+1)
      obs['mission'] = np.zeros((self.max_length, self.max_length), dtype=np.uint8)
      for idx, s in enumerate(split):
        obs['mission'][idx, :len(s)] = s
    else:

      obs['mission'] = np.zeros((1, self.max_length), dtype=np.uint8)
      obs['mission'][0, :len(mission)] = mission
    return obs

class RGBImgFullyObsWrapper(gym.core.ObservationWrapper):
  """
  Wrapper to use fully observable RGB image as the only observation output
  This can be used to have the agent to solve the gridworld in pixel space.
  It removes the direction key from the observation but keeps everything else.
  """

  def __init__(self, env, tile_size=8):
    super().__init__(env)

    self.tile_size = tile_size

    obs_shape = env.observation_space.spaces['image'].shape
    self.observation_space.spaces['image'] = gym.spaces.Box(
        low=0,
        high=255,
        shape=(obs_shape[0] * tile_size, obs_shape[1] * tile_size, 3),
        dtype='uint8'
    )
    raise NotImplemented("currently has bug")

  def observation(self, obs):
    env = self.unwrapped

    rgb_img = env.render(
        obs['image'],
        tile_size=self.tile_size,
        highlight=False
    )

    keys = obs.keys()
    new_obs = dict()
    for k in keys:
        if k == "direction": continue
        new_obs[k] = obs[k]
    new_obs['image'] = rgb_img
    return new_obs


class RGBImgPartialObsWrapper(gym.core.ObservationWrapper):
  """
  Wrapper to use partially observable RGB image as the only observation output
  This can be used to have the agent to solve the gridworld in pixel space.
  It removes the direction key from the observation but keeps everything else.
  """

  def __init__(self, env, tile_size=8):
    super().__init__(env)

    self.tile_size = tile_size

    obs_shape = env.observation_space.spaces['image'].shape
    self.observation_space.spaces['image'] = gym.spaces.Box(
        low=0,
        high=255,
        shape=(obs_shape[0] * tile_size, obs_shape[1] * tile_size, 3),
        dtype='uint8'
    )

  def observation(self, obs):
    env = self.unwrapped

    rgb_img_partial = env.get_obs_render(
        obs['image'],
        tile_size=self.tile_size
    )

    keys = obs.keys()
    new_obs = dict()
    for k in keys:
        if k == "direction": continue
        new_obs[k] = obs[k]
    new_obs['image'] = rgb_img_partial
    return new_obs
