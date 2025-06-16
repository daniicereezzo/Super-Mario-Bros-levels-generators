#!/bin/bash

# Add the conda path to the PATH
#export PATH="/opt/anaconda/anaconda3/bin:$PATH"
#export PATH="/opt/anaconda/bin:$PATH"
export PATH="/home/daniicereezzo/miniforge3/bin:$PATH"

# Activate the conda shell
eval "$(conda shell.bash hook)"

# Set the path to the conda environment
#conda_env_path="/mnt/homeGPU/dcerezo/condaenvs/env_promp"
conda_env_path="env_promp"

# Set the TFHUB_CACHE_DIR to the current directory
export TFHUB_CACHE_DIR=.

# Activate the conda environment
conda activate $conda_env_path

# Get the JDK home path
#JAVA_HOME="java-8-openjdk-amd64"

# Set the seed
seed=2024

# Set the number of levels to generate
n_levels=200

# Print java version
#java -version

# Generate the levels with ProMP
#java -jar ProMP.jar $seed $n_levels

# Create the bin directory
mkdir -p bin

# Compile the java code
javac -d bin -cp "lib/*" $(find src -name "*.java")

# Generate the levels with ProMP
java -cp "bin:lib/*" generate $seed $n_levels