from ray import tune

def get(search, agent):
  if search == 'r2d1':
    space = [
        {
          "seed": tune.grid_search([1]),
          "agent": tune.grid_search(['r2d1']),
          "max_number_of_steps": tune.grid_search([15_000_000]),
          'setting': tune.grid_search(['procgen_easy', 'procgen_easy_medium']),
          "group": tune.grid_search(['r2d1_procgen-2']),
          # 'min_replay_size': tune.grid_search([100, 10_000]),
          # 'importance_sampling_exponent': tune.grid_search([0, .6]),
          # 'out_q_layers': tune.grid_search([1, 2]),
        },
        # {
        #   "seed": tune.grid_search([1]),
        #   "agent": tune.grid_search(['r2d1']),
        #   "max_number_of_steps": tune.grid_search([30_000_000]),
        #   'setting': tune.grid_search(['procgen_easy']),
        #   'min_replay_size': tune.grid_search([100]),
        # }
    ]

  elif search == 'r2d1_procgen_easy':
    space = [
        {
          "seed": tune.grid_search([1]),
          "agent": tune.grid_search(['r2d1']),
          "max_number_of_steps": tune.grid_search([10_000_000]),
          'setting': tune.grid_search([
            'procgen_easy',
            'procgen_easy_medium'
            # 'procgen_easy_hard',
            ]),
          "group": tune.grid_search(['r2d1_procgen-2']),
        }
    ]

  elif search == 'r2d1_taskgen_easy':
    space = [
        {
          "seed": tune.grid_search([1, 2, 3, 4]),
          "agent": tune.grid_search(['r2d1']),
          "group": tune.grid_search(['taskgen_easy-6']),
          "max_number_of_steps": tune.grid_search([10_000_000]),
          'setting': tune.grid_search(['taskgen_long_easy2']),
          # 'importance_sampling_exponent': tune.grid_search([0.0, 0.6]),
          # 'r2d1_loss': tune.grid_search(['n_step_q_learning']),
        }
    ]

  elif search == 'usfa_taskgen_easy':
    space = [
        {
          "seed": tune.grid_search([1, 2, 3, 4]),
          "agent": tune.grid_search(['usfa_lstm']),
          "max_number_of_steps": tune.grid_search([10_000_000]),
          'setting': tune.grid_search(['taskgen_long_easy2']),
          "group": tune.grid_search(['taskgen_easy-6']),
          'value_coeff': tune.grid_search([.5]),
          'eval_task_support': tune.grid_search(['train']),
        }
    ]
  elif search == 'msf_taskgen_easy':
    space = [
        {
          "seed": tune.grid_search([1]),
          "agent": tune.grid_search(['msf']),
          "max_number_of_steps": tune.grid_search([10_000_000]),
          'setting': tune.grid_search(['taskgen_long_easy2']),
          "group": tune.grid_search(['taskgen_easy-6']),
          'value_coeff': tune.grid_search([.5]),
          'reward_coeff': tune.grid_search([0.1, 1.0, 10.0, 50.0]),
          'sf_share_output': tune.grid_search([False]),
        }
    ]

  else:
    raise NotImplementedError(search)


  return space
