from ray import tune

def get(search, agent=''):
  agent = agent or 'r2d1'
  if search == 'slice5':
    space = [
      { # 6
        "seed": tune.grid_search([1, 2, 3]),
        "agent": tune.grid_search([agent]),
        "setting": tune.grid_search(['place_sliced']),
        "max_number_of_steps": tune.grid_search([40_000_000]),
      },
    ]
  elif search == 'place_sliced':
    """
    Next:
    """
    space = [
      { # 6
        "seed": tune.grid_search([1]),
        "agent": tune.grid_search(['usfa_lstm', 'r2d1', 'msf']),
        "setting": tune.grid_search(['place_sliced']),
        "max_number_of_steps": tune.grid_search([40_000_000]),
      },
    ]
  elif search == 'similar5':
    space = [
      { # 6
        "seed": tune.grid_search([1, 2, 3]),
        "agent": tune.grid_search([agent]),
        "setting": tune.grid_search(['similar']),
        "max_number_of_steps": tune.grid_search([30_000_000]),
      },
    ]
  elif search == 'cook5':
    space = [
      { # 6
        "seed": tune.grid_search([1, 2, 3]),
        "agent": tune.grid_search([agent]),
        "setting": tune.grid_search(['cook']),
        "max_number_of_steps": tune.grid_search([30_000_000]),
      },
    ]

  elif search == 'gen6_r2d1':
    space = [
      { # 6
        "seed": tune.grid_search([1]),
        "setting": tune.grid_search(['genv6']),
        "agent": tune.grid_search([agent]),
        "task_reps": tune.grid_search(['object_noand_verbose']),
        "max_number_of_steps": tune.grid_search([40_000_000]),
      } for s in [1,2]
    ]
  elif search == 'gen6_usfa':
    space = [
      { # 6
        "seed": tune.grid_search([1,2]),
        "setting": tune.grid_search(['genv6']),
        "agent": tune.grid_search(['usfa_lstm']),
        "embed_task_dim": tune.grid_search([16]),
        "value_coeff": tune.grid_search([.5]),
        "reward_coeff": tune.grid_search([50]),
        "task_reps": tune.grid_search(['object_noand_verbose']),
        "max_number_of_steps": tune.grid_search([40_000_000]),
      },
      { # 6
        "seed": tune.grid_search([1,2]),
        "setting": tune.grid_search(['genv6']),
        "agent": tune.grid_search(['usfa_lstm']),
        "embed_task_dim": tune.grid_search([16]),
        "value_coeff": tune.grid_search([.5]),
        "reward_coeff": tune.grid_search([10]),
        "task_reps": tune.grid_search(['object_noand_verbose']),
        "max_number_of_steps": tune.grid_search([40_000_000]),
      },
      { # 6
        "seed": tune.grid_search([1,2]),
        "setting": tune.grid_search(['genv6']),
        "agent": tune.grid_search(['usfa_lstm']),
        "embed_task_dim": tune.grid_search([8]),
        "value_coeff": tune.grid_search([.5]),
        "reward_coeff": tune.grid_search([50]),
        "task_reps": tune.grid_search(['object_noand_verbose']),
        "max_number_of_steps": tune.grid_search([40_000_000]),
      },
      { # 6
        "seed": tune.grid_search([1,2]),
        "setting": tune.grid_search(['genv6']),
        "agent": tune.grid_search(['usfa_lstm']),
        "embed_task_dim": tune.grid_search([8]),
        "value_coeff": tune.grid_search([.5]),
        "reward_coeff": tune.grid_search([10]),
        "task_reps": tune.grid_search(['object_noand_verbose']),
        "max_number_of_steps": tune.grid_search([40_000_000]),
      },
    ]
  elif search == 'gen6_msf_reward':
    space = [
      { # 6
        "seed": tune.grid_search([1]),
        "setting": tune.grid_search(['genv6']),
        "agent": tune.grid_search([agent]),
        "nmodules": tune.grid_search([4]),
        "module_task_dim": tune.grid_search([1]),
        "value_coeff": tune.grid_search([.5]),
        "reward_coeff": tune.grid_search([10]),
        "task_reps": tune.grid_search(['object_noand_verbose']),
        "max_number_of_steps": tune.grid_search([40_000_000]),
      },
      { # 6
        "seed": tune.grid_search([1]),
        "setting": tune.grid_search(['genv6']),
        "agent": tune.grid_search([agent]),
        "nmodules": tune.grid_search([8]),
        "module_task_dim": tune.grid_search([1]),
        "value_coeff": tune.grid_search([.5]),
        "reward_coeff": tune.grid_search([10]),
        "task_reps": tune.grid_search(['object_noand_verbose']),
        "max_number_of_steps": tune.grid_search([40_000_000]),
      },
      { # 6
        "seed": tune.grid_search([1]),
        "setting": tune.grid_search(['genv6']),
        "agent": tune.grid_search([agent]),
        "nmodules": tune.grid_search([8]),
        "module_task_dim": tune.grid_search([1]),
        "task_reps": tune.grid_search(['object_noand_verbose']),
        "value_coeff": tune.grid_search([.5]),
        "reward_coeff": tune.grid_search([50]),
        "max_number_of_steps": tune.grid_search([40_000_000]),
      },
      { # 6
        "seed": tune.grid_search([1]),
        "setting": tune.grid_search(['genv6']),
        "agent": tune.grid_search([agent]),
        "nmodules": tune.grid_search([4]),
        "module_task_dim": tune.grid_search([1]),
        "task_reps": tune.grid_search(['object_noand_verbose']),
        "value_coeff": tune.grid_search([.5]),
        "reward_coeff": tune.grid_search([50]),
        "max_number_of_steps": tune.grid_search([40_000_000]),
      }
    ]
  elif search == 'gen6_msf_size_r10':
    space = [
      { # 6
        "seed": tune.grid_search([1]),
        "setting": tune.grid_search(['genv6']),
        "agent": tune.grid_search([agent]),
        "nmodules": tune.grid_search([4]),
        "module_task_dim": tune.grid_search([4]),
        "value_coeff": tune.grid_search([.5]),
        "reward_coeff": tune.grid_search([10.0]),
        "task_reps": tune.grid_search(['object_noand_verbose']),
        "max_number_of_steps": tune.grid_search([40_000_000]),
      },
      { # 6
        "seed": tune.grid_search([1]),
        "setting": tune.grid_search(['genv6']),
        "agent": tune.grid_search([agent]),
        "nmodules": tune.grid_search([2]),
        "module_task_dim": tune.grid_search([8]),
        "value_coeff": tune.grid_search([.5]),
        "reward_coeff": tune.grid_search([10.0]),
        "task_reps": tune.grid_search(['object_noand_verbose']),
        "max_number_of_steps": tune.grid_search([40_000_000]),
      },
      { # 6
        "seed": tune.grid_search([1]),
        "setting": tune.grid_search(['genv6']),
        "agent": tune.grid_search([agent]),
        "nmodules": tune.grid_search([8]),
        "module_task_dim": tune.grid_search([2]),
        "task_reps": tune.grid_search(['object_noand_verbose']),
        "value_coeff": tune.grid_search([.5]),
        "reward_coeff": tune.grid_search([10.0]),
        "max_number_of_steps": tune.grid_search([40_000_000]),
      },
      { # 6
        "seed": tune.grid_search([1]),
        "setting": tune.grid_search(['genv6']),
        "agent": tune.grid_search([agent]),
        "nmodules": tune.grid_search([4]),
        "module_task_dim": tune.grid_search([2]),
        "task_reps": tune.grid_search(['object_noand_verbose']),
        "value_coeff": tune.grid_search([.5]),
        "reward_coeff": tune.grid_search([10.0]),
        "max_number_of_steps": tune.grid_search([40_000_000]),
      }
    ]
  elif search == 'gen6_msf_size_r50':
    space = [
      { # 6
        "seed": tune.grid_search([1]),
        "setting": tune.grid_search(['genv6']),
        "agent": tune.grid_search([agent]),
        "nmodules": tune.grid_search([4]),
        "module_task_dim": tune.grid_search([4]),
        "value_coeff": tune.grid_search([.5]),
        "reward_coeff": tune.grid_search([50.0]),
        "task_reps": tune.grid_search(['object_noand_verbose']),
        "max_number_of_steps": tune.grid_search([40_000_000]),
      },
      { # 6
        "seed": tune.grid_search([1]),
        "setting": tune.grid_search(['genv6']),
        "agent": tune.grid_search([agent]),
        "nmodules": tune.grid_search([2]),
        "module_task_dim": tune.grid_search([8]),
        "value_coeff": tune.grid_search([.5]),
        "reward_coeff": tune.grid_search([50.0]),
        "task_reps": tune.grid_search(['object_noand_verbose']),
        "max_number_of_steps": tune.grid_search([40_000_000]),
      },
      { # 6
        "seed": tune.grid_search([1]),
        "setting": tune.grid_search(['genv6']),
        "agent": tune.grid_search([agent]),
        "nmodules": tune.grid_search([8]),
        "module_task_dim": tune.grid_search([2]),
        "task_reps": tune.grid_search(['object_noand_verbose']),
        "value_coeff": tune.grid_search([.5]),
        "reward_coeff": tune.grid_search([50.0]),
        "max_number_of_steps": tune.grid_search([40_000_000]),
      },
      { # 6
        "seed": tune.grid_search([1]),
        "setting": tune.grid_search(['genv6']),
        "agent": tune.grid_search([agent]),
        "nmodules": tune.grid_search([4]),
        "module_task_dim": tune.grid_search([2]),
        "task_reps": tune.grid_search(['object_noand_verbose']),
        "value_coeff": tune.grid_search([.5]),
        "reward_coeff": tune.grid_search([50.0]),
        "max_number_of_steps": tune.grid_search([40_000_000]),
      }
    ]




  elif search == 'modr2d1':
    """
    Next:
    """
    space = [
      { # 6
        "seed": tune.grid_search([1]),
        "agent": tune.grid_search(['modr2d1']),
        "setting": tune.grid_search(['pickup']),
        "struct_w": tune.grid_search([False, True]),
        "nmodules": tune.grid_search([4]),
        "dot_qheads": tune.grid_search([False, True]),
        "max_number_of_steps": tune.grid_search([2_000_000]),
      },
    ]

  elif search == 'test8':
    """
    Next:
    """
    space = [
      {
        "seed": tune.grid_search([1]),
        "agent": tune.grid_search(['msf']),
        "setting": tune.grid_search(['gen_simple']),
        "task_reps": tune.grid_search(['object_verbose']),
        "activation": tune.grid_search([t]),
        "struct_and": tune.grid_search([True]),
        "value_coeff": tune.grid_search([.5]),
        "max_number_of_steps": tune.grid_search([10_000_000]),
      } for t in ['sigmoid', 'tanh']
    ] + [
      {
        "seed": tune.grid_search([1]),
        "agent": tune.grid_search(['msf']),
        "setting": tune.grid_search(['gen_simple']),
        "task_reps": tune.grid_search(['object_verbose']),
        "activation": tune.grid_search([t]),
        "struct_and": tune.grid_search([True]),
        "value_coeff": tune.grid_search([.5]),
        "w_l1_coeff": tune.grid_search([1e-4]),
        "max_number_of_steps": tune.grid_search([10_000_000]),
      } for t in ['sigmoid', 'tanh']
    ] + [
      {
        "seed": tune.grid_search([1]),
        "agent": tune.grid_search(['msf']),
        "setting": tune.grid_search(['gen_simple']),
        "task_reps": tune.grid_search(['object_verbose']),
        "activation": tune.grid_search([t]),
        "struct_and": tune.grid_search([True]),
        "value_coeff": tune.grid_search([.5]),
        "w_l1_coeff": tune.grid_search([1e-3]),
        "max_number_of_steps": tune.grid_search([10_000_000]),
      } for t in ['sigmoid', 'tanh']
    ]

  elif search == 'test9_r2d1':
    """
    Next:
    """
    space = [
      {
        "seed": tune.grid_search([1, 2]),
        "group": tune.grid_search(['test9']),
        "agent": tune.grid_search(['r2d1']),
        "setting": tune.grid_search(['genv5']),
        "task_reps": tune.grid_search(['object_verbose']),
        "struct_and": tune.grid_search([True]),
        "max_number_of_steps": tune.grid_search([20_000_000]),
      },
      {
        "seed": tune.grid_search([1, 2]),
        "group": tune.grid_search(['test9']),
        "agent": tune.grid_search(['r2d1']),
        "setting": tune.grid_search(['genv5']),
        "task_reps": tune.grid_search(['object_verbose']),
        "struct_and": tune.grid_search([False]),
        "max_number_of_steps": tune.grid_search([20_000_000]),
      },
      {
        "seed": tune.grid_search([1, 2]),
        "group": tune.grid_search(['test9']),
        "agent": tune.grid_search(['r2d1']),
        "setting": tune.grid_search(['gen_simple']),
        "task_reps": tune.grid_search(['object_verbose']),
        "struct_and": tune.grid_search([True]),
        "max_number_of_steps": tune.grid_search([20_000_000]),
      },
    ]
  elif search == 'test9_gen5_gru':
    """
    Next:
    """
    space = [
      {
        "seed": tune.grid_search([1, 2]),
        "group": tune.grid_search(['test9']),
        "agent": tune.grid_search(['msf']),
        "setting": tune.grid_search(['genv5']),
        "task_reps": tune.grid_search(['object_verbose']),
        "struct_and": tune.grid_search([False]),
        "activation": tune.grid_search(['none']),
        "max_number_of_steps": tune.grid_search([30_000_000]),
      },
      {
        "seed": tune.grid_search([1, 2]),
        "group": tune.grid_search(['test9']),
        "agent": tune.grid_search(['msf']),
        "setting": tune.grid_search(['genv5']),
        "task_reps": tune.grid_search(['object_verbose']),
        "struct_and": tune.grid_search([False]),
        "activation": tune.grid_search(['sigmoid']),
        "w_l1_coeff": tune.grid_search([1e-3]),
        "max_number_of_steps": tune.grid_search([30_000_000]),
      },
      {
        "seed": tune.grid_search([1, 2]),
        "group": tune.grid_search(['test9']),
        "agent": tune.grid_search(['usfa_lstm']),
        "setting": tune.grid_search(['genv5']),
        "task_reps": tune.grid_search(['object_verbose']),
        "struct_and": tune.grid_search([False]),
        "max_number_of_steps": tune.grid_search([30_000_000]),
      },
      {
        "seed": tune.grid_search([1, 2]),
        "group": tune.grid_search(['test9']),
        "agent": tune.grid_search(['msf']),
        "setting": tune.grid_search(['genv5']),
        "task_reps": tune.grid_search(['object_verbose']),
        "struct_and": tune.grid_search([False]),
        "phi_l1_coeff": tune.grid_search([1e-4]),
        "max_number_of_steps": tune.grid_search([30_000_000]),
      },
    ]
  elif search == 'test9_gen5_sum':
    """
    Next:
    """
    space = [
      {
        "seed": tune.grid_search([1, 2]),
        "group": tune.grid_search(['test9']),
        "agent": tune.grid_search(['msf']),
        "setting": tune.grid_search(['genv5']),
        "task_reps": tune.grid_search(['object_verbose']),
        "struct_and": tune.grid_search([True]),
        "activation": tune.grid_search(['none']),
        "max_number_of_steps": tune.grid_search([30_000_000]),
      },
      {
        "seed": tune.grid_search([1, 2]),
        "group": tune.grid_search(['test9']),
        "agent": tune.grid_search(['msf']),
        "setting": tune.grid_search(['genv5']),
        "task_reps": tune.grid_search(['object_verbose']),
        "struct_and": tune.grid_search([True]),
        "activation": tune.grid_search(['sigmoid']),
        "w_l1_coeff": tune.grid_search([1e-3]),
        "max_number_of_steps": tune.grid_search([30_000_000]),
      },
      {
        "seed": tune.grid_search([1, 2]),
        "group": tune.grid_search(['test9']),
        "agent": tune.grid_search(['usfa_lstm']),
        "setting": tune.grid_search(['genv5']),
        "task_reps": tune.grid_search(['object_verbose']),
        "struct_and": tune.grid_search([True]),
        "max_number_of_steps": tune.grid_search([30_000_000]),
      },
      {
        "seed": tune.grid_search([1, 2]),
        "group": tune.grid_search(['test9']),
        "agent": tune.grid_search(['msf']),
        "setting": tune.grid_search(['genv5']),
        "task_reps": tune.grid_search(['object_verbose']),
        "struct_and": tune.grid_search([True]),
        "phi_l1_coeff": tune.grid_search([1e-4]),
        "max_number_of_steps": tune.grid_search([30_000_000]),
      },
    ]
  elif search == 'test9_simple_sum':
    """
    Next:
    """
    space = [
      {
        "seed": tune.grid_search([1]),
        "group": tune.grid_search(['test9']),
        "agent": tune.grid_search(['msf']),
        "setting": tune.grid_search(['gen_simple']),
        "task_reps": tune.grid_search(['object_verbose']),
        "struct_and": tune.grid_search([True]),
        "memory_size": tune.grid_search([512]),
        "nmodules": tune.grid_search([8]),
        "max_number_of_steps": tune.grid_search([30_000_000]),
      },
      {
        "seed": tune.grid_search([1]),
        "group": tune.grid_search(['test9']),
        "agent": tune.grid_search(['msf']),
        "setting": tune.grid_search(['gen_simple']),
        "task_reps": tune.grid_search(['object_verbose']),
        "module_task_dim": tune.grid_search([4]),
        "struct_and": tune.grid_search([True]),
        "memory_size": tune.grid_search([512]),
        "max_number_of_steps": tune.grid_search([30_000_000]),
      },
      {
        "seed": tune.grid_search([1]),
        "group": tune.grid_search(['test9']),
        "agent": tune.grid_search(['msf']),
        "setting": tune.grid_search(['gen_simple']),
        "task_reps": tune.grid_search(['object_verbose']),
        "module_task_dim": tune.grid_search([4]),
        "struct_and": tune.grid_search([True]),
        "stop_w_grad": tune.grid_search([True]),
        "max_number_of_steps": tune.grid_search([30_000_000]),
      },
      {
        "seed": tune.grid_search([1]),
        "group": tune.grid_search(['test9']),
        "agent": tune.grid_search(['msf']),
        "setting": tune.grid_search(['gen_simple']),
        "task_reps": tune.grid_search(['object_verbose']),
        "module_task_dim": tune.grid_search([4]),
        "struct_and": tune.grid_search([True]),
        "stop_w_grad": tune.grid_search([True]),
        "seperate_value_params": tune.grid_search([True]),
        "max_number_of_steps": tune.grid_search([30_000_000]),
      },

      # {
      #   "seed": tune.grid_search([1]),
      #   "group": tune.grid_search(['test9']),
      #   "agent": tune.grid_search(['msf']),
      #   "setting": tune.grid_search(['gen_simple']),
      #   "task_reps": tune.grid_search(['object_verbose']),
      #   "struct_and": tune.grid_search([True]),
      #   "memory_size": tune.grid_search([1024]),
      #   "max_number_of_steps": tune.grid_search([30_000_000]),
      # },
      # {
      #   "seed": tune.grid_search([1]),
      #   "group": tune.grid_search(['test9']),
      #   "agent": tune.grid_search(['usfa_lstm']),
      #   "setting": tune.grid_search(['gen_simple']),
      #   "task_reps": tune.grid_search(['object_verbose']),
      #   "struct_and": tune.grid_search([True]),
      #   "memory_size": tune.grid_search([512]),
      #   "max_number_of_steps": tune.grid_search([30_000_000]),
      # },
      # {
      #   "seed": tune.grid_search([1]),
      #   "group": tune.grid_search(['test9']),
      #   "agent": tune.grid_search(['usfa_lstm']),
      #   "setting": tune.grid_search(['gen_simple']),
      #   "task_reps": tune.grid_search(['object_verbose']),
      #   "struct_and": tune.grid_search([True]),
      #   "memory_size": tune.grid_search([1024]),
      #   "max_number_of_steps": tune.grid_search([30_000_000]),
      # },
    ]
  elif search == 'test9_targets':
    """
    Next:
    """
    space = [
      {
        "seed": tune.grid_search([1]),
        "agent": tune.grid_search(['msf']),
        "setting": tune.grid_search(['gen_simple']),
        "task_reps": tune.grid_search(['object_verbose']),
        "struct_and": tune.grid_search([True]),
        "target_phi": tune.grid_search([True]),
        "phi_l1_coeff": tune.grid_search([t]),
        "max_number_of_steps": tune.grid_search([30_000_000]),
      } for t in [1e-3, 1e-4]] + [
      {
        "seed": tune.grid_search([1]),
        "agent": tune.grid_search(['msf']),
        "setting": tune.grid_search(['gen_simple']),
        "task_reps": tune.grid_search(['object_verbose']),
        "struct_and": tune.grid_search([True]),
        "target_phi": tune.grid_search([True]),
        "seperate_value_params": tune.grid_search([True]),
        # "out_hidden_size": tune.grid_search([128]),
        "phi_l1_coeff": tune.grid_search([t]),
        "max_number_of_steps": tune.grid_search([30_000_000]),
      } for t in [1e-3, 1e-4] ]

  else:
    raise NotImplementedError(search)

  return space