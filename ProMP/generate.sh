#!/bin/bash

# TODO: Add the conda path to the PATH
# Example: export PATH="/opt/anaconda/anaconda3/bin:$PATH"
export PATH="your_path_to_conda:$PATH"

# Activate the conda shell
eval "$(conda shell.bash hook)"

# TODO: Set the path to the conda environment
# Example: conda_env_path="env_promp"
conda_env_path="your_conda_environment_name"

# Set the TFHUB_CACHE_DIR to the current directory
export TFHUB_CACHE_DIR=.

# Activate the conda environment
conda activate $conda_env_path

# TODO: Set the seed
# Example: seed=2024
seed=your_seed

# Set the number of levels to generate
# Example: n_levels=200
n_levels=your_number_of_levels

# Create the bin directory
mkdir -p bin

# Compile the java code
javac -d bin -cp "lib/*" $(find src -name "*.java")

# Generate the levels with ProMP
java -cp "bin:lib/*" generate $seed $n_levels
