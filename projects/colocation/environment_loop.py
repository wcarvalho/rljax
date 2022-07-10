import operator
import time

import acme
from acme.utils import loggers

from dm_env import specs
import numpy as np
import tree

"""
For debugging purposes only. You can rprint stuff here to check that things are working ok
"""
def _generate_zeros_from_spec(spec: specs.Array) -> np.ndarray:
  return np.zeros(spec.shape, spec.dtype)


class EnvironmentLoop(acme.EnvironmentLoop):
  # def __init__(self, *args, metric_fn=None, **kwargs):
  #   self.metric_fn = metric_fn or default_metric_fn
  def run_episode(self) -> loggers.LoggingData:
    """Run one episode.

    Each episode is a loop which interacts first with the environment to get an
    observation and then give that observation to the agent in order to retrieve
    an action.

    Returns:
      An instance of `loggers.LoggingData`.
    """
    # Reset any counts and start the environment.
    start_time = time.time()
    episode_steps = 0

    # For evaluation, this keeps track of the total undiscounted reward
    # accumulated during the episode.
    episode_return = tree.map_structure(_generate_zeros_from_spec,
                                        self._environment.reward_spec())
    timestep = self._environment.reset()

    task_returns = [tree.map_structure(_generate_zeros_from_spec,
                                        self._environment.reward_spec()) for _ in range(self._environment.env.num_objects)]

    # Make the first observation.
    self._actor.observe_first(timestep)

    #TODO: Get rid of this
    all_observations = []
    all_rewards = []
    all_tasks = []
    all_actions = []

    # Run an episode.
    while not timestep.last():
      # Generate an action from the agent's policy and step the environment.
      action = self._actor.select_action(timestep.observation)
      timestep = self._environment.step(action)

      # Have the agent observe the timestep and let the actor update itself.
      self._actor.observe(action, next_timestep=timestep)
      if self._should_update:
        self._actor.update()

      # Book-keeping.
      episode_steps += 1

      # Equivalent to: episode_return += timestep.reward
      # We capture the return value because if timestep.reward is a JAX
      # DeviceArray, episode_return will not be mutated in-place. (In all other
      # cases, the returned episode_return will be the same object as the
      # argument episode_return.)
      episode_return = tree.map_structure(operator.iadd,
                                          episode_return,
                                          timestep.reward)

      index = np.argmax(timestep.observation.observation.task)
      task_returns[index] = tree.map_structure(operator.iadd,
                                          task_returns[index],
                                          timestep.reward)

      # TODO: Get rid of this

      # print(dir(timestep.observation.observation))
      # np.savez("/home/nameer/successor_features/rljax/results/ENVOUT.npz",img=timestep.observation.observation.image,task=timestep.observation.observation.task)
      all_observations.append(timestep.observation.observation.image)
      all_rewards.append(timestep.reward)
      all_tasks.append(timestep.observation.observation.task)
      all_actions.append(action)

    # Record counts.
    counts = self._counter.increment(episodes=1, steps=episode_steps)

    level = self._environment.env.current_levelname
    print("Level: " + str(level))
    print("Room: " + str(self._environment.env.room))
    # Collect the results and combine with counts.
    steps_per_second = episode_steps / (time.time() - start_time)
    result = {
        f'0.task/{level}/episode_return': episode_return,
        'steps_per_second' : steps_per_second,
        'episode_length': episode_steps,
    }
    for idx, return_val in enumerate(task_returns):
        result['task_return' + str(idx)] = return_val
    result.update(counts)


    #randomly write an episode to a file every 20ish episodes
    # print(self._counter.get_counts())
    # if np.random.uniform(0,1)<.05:
    #     fname = '/home/nameer/successor_features/rljax/results/env_images/' + str(np.random.random()) + '.npz'
    #     np.savez(fname,images=np.asarray(all_observations),tasks=np.asarray(all_tasks), rewards=np.asarray(all_rewards),actions=np.asarray(all_actions))

    return result
