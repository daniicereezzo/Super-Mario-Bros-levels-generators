#!/bin/bash

# Add the conda path to the PATH
export PATH="/opt/anaconda/anaconda3/bin:$PATH"
export PATH="/opt/anaconda/bin:$PATH"
#export PATH="/home/daniicereezzo/miniforge3/bin:$PATH"

# Activate the conda shell
eval "$(conda shell.bash hook)"

# Set the path to the conda environment
conda_env_path="/mnt/homeGPU/dcerezo/condaenvs/env_mariogan"
#conda_env_path="env_mariogan"

# Set the TFHUB_CACHE_DIR to the current directory
export TFHUB_CACHE_DIR=.

# Activate the conda environment
conda activate $conda_env_path

# Print python and pip versions
#python --version
#pip --version

# Set seed
seed=2024

# Train the GAN
#python -u train.py --seed $seed --cuda

# Generate the levels with GAN
python -u generate_random.py --seed $seed

# Generate the levels with MarioGAN
python -u generate_cma.py --seed $seed