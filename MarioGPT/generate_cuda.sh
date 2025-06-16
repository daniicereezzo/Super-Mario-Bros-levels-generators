#!/bin/bash

# Add the conda path to the PATH
export PATH="/opt/anaconda/anaconda3/bin:$PATH"
export PATH="/opt/anaconda/bin:$PATH"
#export PATH="/home/daniicereezzo/miniforge3/bin:$PATH"

# Activate the conda shell
eval "$(conda shell.bash hook)"

# Set the path to the conda environment
conda_env_path="/mnt/homeGPU/dcerezo/condaenvs/env_mariogpt"
#conda_env_path="env_ga2024"

# Set the TFHUB_CACHE_DIR to the current directory
export TFHUB_CACHE_DIR=.
export TRANSFORMERS_CACHE=.

# Activate the conda environment
conda activate $conda_env_path

# Print python and pip versions
#python --version
#pip --version

# Set the seed
seed=2024

# Set the number of levels to generate
n_levels=200

# Generate the levels with MarioGPT
python -u generate_cuda.py --seed $seed --n_levels $n_levels