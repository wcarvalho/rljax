from babyai.bot import Bot, GoNextToSubgoal
from gym_minigrid.minigrid import *
from babyai.levels.verifier import *
from babyai.levels.verifier import (ObjDesc, pos_next_to,
                                    GoToInstr, OpenInstr, PickupInstr, PutNextInstr, BeforeInstr, AndInstr, AfterInstr)

from envs.babyai_kitchen.levelgen import KitchenLevel

class KitchenBot(Bot):
  """docstring for KitchenBot"""
  def __init__(self, env : KitchenLevel):

    # Mission to be solved
    self.mission = mission = env

    # Grid containing what has been mapped out
    self.grid = Grid(mission.width, mission.height)

    # Visibility mask. True for explored/seen, false for unexplored.
    self.vis_mask = np.zeros(shape=(mission.width, mission.height), dtype=np.bool)

    # Stack of tasks/subtasks to complete (tuples)
    self.subgoals = subgoals = self.mission.task.subgoals()
    self.stack = [GoNextToSubgoal(self, tuple(subgoal.goto.cur_pos)) for subgoal in subgoals]
    self.stack.reverse()

    self.original_size = len(self.stack)
    # How many BFS searches this bot has performed
    self.bfs_counter = 0

    # How many steps were made in total in all BFS searches
    # performed by this bot
    self.bfs_step_counter = 0


  def generate_traj(self, action_taken=None, plot_fn=lambda x:x):

    steps_left = len(self.stack)
    env = self.mission

    all_obs = []
    all_action = []
    all_reward = []
    all_done = []

    def step_update(_action):
      _obs, _reward, _done, _info = env.step(_action)
      all_obs.append(_obs)
      all_action.append(_action)
      all_reward.append(_reward)
      all_done.append(_done)
      return _obs, _reward, _done, _info

    idx = 0
    while self.stack:
      idx += 1
      if idx > 1000:
        raise RuntimeError("Taking too long")

      action = self.replan(action_taken)

      # -----------------------
      # done??
      # -----------------------
      if action == env.actions.done:
        return all_obs, all_action, all_reward, all_done

      # -----------------------
      # take actions
      # -----------------------
      obs, reward, done, info = step_update(action)

      plot_fn(obs)

      # -----------------------
      # subgoal object in front? do actions
      # -----------------------
      subgoal_idx = self.original_size - steps_left
      subgoal = self.subgoals[subgoal_idx]
      subgoal_object = subgoal.goto
      object_infront = env.grid.get(*env.front_pos)


      if object_infront and object_infront.type == subgoal.goto.type:
        for action_str in subgoal.actions:
          interaction = env.actiondict[action_str]
          obs, reward, done, info = step_update(interaction)

          plot_fn(obs)

      # -----------------------
      # book-keeping
      # -----------------------
      steps_left = len(self.stack)
      action_taken = action



  def _check_erroneous_box_opening(self, action):
    # ignore this
    pass