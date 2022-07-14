#!/bin/bash

if [[ $1 = gpu ]]; then
  arch=gpu_procgen_minihack
elif [[ $1 = cpu ]]; then
  arch=cpu
else
  echo 'incorrect arg'
  exit
fi

conda create -n acmejax python=3.9 --force

eval "$(conda shell.bash hook)"
conda activate acmejax

##############################################
# For Minihack
##############################################
# missing: libbz2-dev build-essential ninja-build software-properties-common
conda install -c anaconda cmake
conda install -c conda-forge bison

export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${HOME}/miniconda3/envs/acmejax/lib/

##############################################
# Main installation
##############################################
conda env update --name acmejax --file $arch.yaml

conda install -c anaconda cudnn==8.2.1 --force

##############################################
# ACME
##############################################
git clone https://github.com/deepmind/acme.git _acme
cd _acme
# git checkout 6e1d71104371998e8cd0143cb8090c24263c50c4 # 3.0.0
git checkout e7e99762369c2ab2871d1c4bc6b6ab776eddf48c # 4.0.0
pip install --editable .[jax,tf,testing,envs]
cd ..

##############################################
# BabyAI
##############################################
git clone https://github.com/maximecb/gym-minigrid.git _gym-minigrid
git checkout 03cf21f61bce58ab13a1de450f6269edd636183a
cp install/minigrid_setup.py _gym-minigrid/setup.py
cd _gym-minigrid
pip install --editable .
cd ..

git clone https://github.com/mila-iqia/babyai.git _babyai
cp install/babyai_setup.py _babyai/setup.py
cd _babyai
pip install --editable .
cd ..


##############################################
# ProcGen (FruitBot)
##############################################
cd envs/procgen
pip install -e .
cd ../..


##############################################
# JAX (CUDA)
##############################################
if [[ $arch = 'gpu' ]]; then
  pip install --upgrade jax[cuda]==0.2.27 -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
  # EXPECTED ERRORS for jax>=0.2.26
  # 1. rlax 0.1.1 requires <=0.2.21
  # 2. distrax 0.1.0 requires jax<=0.2.21,

fi
