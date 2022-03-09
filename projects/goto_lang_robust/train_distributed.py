"""
Run Successor Feature based agents and baselines on 
  BabyAI derivative environments.

Comand I run:
  PYTHONPATH=$PYTHONPATH:. \
    LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/miniconda3/envs/acmejax/lib/ \
    CUDA_VISIBLE_DEVICES=0 \
    XLA_PYTHON_CLIENT_PREALLOCATE=false \
    TF_FORCE_GPU_ALLOW_GROWTH=true \
    python projects/goto_lang_robust/train_distributed.py \
    --agent r2d1_noise_ensemble
"""

# Do not preallocate GPU memory for JAX.
import os
os.environ['XLA_PYTHON_CLIENT_PREALLOCATE'] = 'false'


import launchpad as lp
from launchpad.nodes.python.local_multi_processing import PythonProcess

from absl import app
from absl import flags
import acme
from acme.utils import paths
import functools

from agents import td_agent
from projects.goto_lang_robust import helpers
from projects.goto_lang_robust.environment_loop import EnvironmentLoop
from utils import make_logger, gen_log_dir
import pickle


# -----------------------
# flags
# -----------------------
flags.DEFINE_string('experiment', None, 'experiment_name.')
flags.DEFINE_string('agent', 'r2d1', 'which agent.')
flags.DEFINE_integer('seed', 1, 'Random seed.')
flags.DEFINE_integer('num_actors', 1, 'Number of actors.')
flags.DEFINE_integer('max_number_of_steps', None, 'Maximum number of steps.')
flags.DEFINE_bool('wandb', False, 'whether to log.')

FLAGS = flags.FLAGS

def build_program(agent, num_actors,
  use_wandb=False,
  setting=1,
  room_size=6,
  num_dists=1,
  instr='goto',
  experiment=None,
  log_every=30.0, # how often to log
  config_kwargs=None, # config
  path='.', # path that's being run from
  log_dir=None,
  hourminute=True):
  # -----------------------
  # load env stuff
  # -----------------------
  environment_factory = lambda is_eval: helpers.make_environment(
    evaluation=is_eval,
    path=path,
    setting=setting,
    room_size=room_size,
    num_dists=num_dists,
    instr=instr,
    )
  env = environment_factory(False)
  max_vocab_size = len(env.env.instr_preproc.vocab) # HACK
  env_spec = acme.make_environment_spec(env)
  del env

  # -----------------------
  # load agent/network stuff
  # -----------------------
  config, NetworkCls, NetKwargs, LossFn, LossFnKwargs = helpers.load_agent_settings(agent, env_spec, config_kwargs,
    setting=setting, max_vocab_size=max_vocab_size)

  batch_size = config.batch_size
  def network_factory(spec):
    return td_agent.make_networks(
      batch_size=batch_size,
      env_spec=env_spec,
      NetworkCls=NetworkCls,
      NetKwargs=NetKwargs,
      eval_network=True)

  builder=functools.partial(td_agent.TDBuilder,
      LossFn=LossFn, LossFnKwargs=LossFnKwargs,
    )

  # -----------------------
  # loggers
  # -----------------------
  agent = str(agent)
  extra = dict(seed=config.seed)
  if experiment:
    extra['exp'] = experiment
  log_dir = log_dir or gen_log_dir(
    base_dir=f"{path}/results/goto_lang_robust/distributed",
    hourminute=hourminute,
    agent=agent,
    **extra)


  logger_fn = lambda : make_logger(
        log_dir=log_dir,
        label='r2d1',
        asynchronous=True)

  actor_logger_fn = lambda actor_id: make_logger(
                  log_dir=log_dir, label='actor',
                  save_data=actor_id == 0,
                  steps_key="actor_steps",
                  )
  evaluator_logger_fn = lambda : make_logger(
                  log_dir=log_dir, label='evaluator',
                  steps_key="evaluator_steps",
                  )

  # -----------------------
  # save config
  # -----------------------
  paths.process_path(log_dir)
  with open(os.path.join(log_dir, 'config.pickle'), 'wb') as handle:
    pickle.dump(config, handle, protocol=pickle.HIGHEST_PROTOCOL)

  # -----------------------
  # build program
  # -----------------------
  return td_agent.DistributedTDAgent(
      environment_factory=environment_factory,
      environment_spec=env_spec,
      network_factory=network_factory,
      builder=builder,
      logger_fn=logger_fn,
      actor_logger_fn=actor_logger_fn,
      evaluator_logger_fn=evaluator_logger_fn,
      EnvLoopCls=EnvironmentLoop,
      config=config,
      workdir=log_dir,
      seed=config.seed,
      num_actors=num_actors,
      max_number_of_steps=config.max_number_of_steps,
      log_every=log_every).build()


def main(_):
  config_kwargs=dict(seed=FLAGS.seed)
  if FLAGS.max_number_of_steps is not None:
    config_kwargs['max_number_of_steps'] = FLAGS.max_number_of_steps
  program = build_program(
    agent=FLAGS.agent,
    num_actors=FLAGS.num_actors,
    experiment=FLAGS.experiment,
    use_wandb=FLAGS.wandb, config_kwargs=config_kwargs)

  # Launch experiment.
  lp.launch(program, lp.LaunchType.LOCAL_MULTI_THREADING,
    terminal='current_terminal',
    local_resources = {
      'actor':
          PythonProcess(env=dict(CUDA_VISIBLE_DEVICES='')),
      'evaluator':
          PythonProcess(env=dict(CUDA_VISIBLE_DEVICES=''))}
  )

if __name__ == '__main__':
  app.run(main)
