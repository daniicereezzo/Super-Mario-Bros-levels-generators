# Super Mario Bros levels generators

## Overview

Repository containing the Super Mario Bros levels generators evaluated in the paper **'From Traditional Methods to GPT-based Models for 2D Video Game Level Procedural Content Generation: An Empirical Study'**.

Each generator contains its own source code in the subfolder identified by its name and has its own specific build and execution instructions.

This README provides some guidelines on how to build and run each project. Nevertheless, each project directory includes a `README.md` file with additional details.

## Prerequisites

Make sure you have installed a `conda` distribution before building and running any project.

## General guidelines

Every generator in this repository follows a similar build process:

1. Create a conda environment for that generator.
2. Activate the environment.
3. Install the generator dependencies if needed (following the specific instructions for each generator).
4. Deactivate the environment.
5. Navigate to the generator subfolder:
6. Complete the `generate.sh` script with the following data:
 - Path of your conda distribution.
 - Name of the environment you created.
 - Seed you want to use for reproducibility.
 - Number of levels you want to generate.
7. Execute the `generate.sh` script to generate the levels.

## Specific instructions for each generator

### ProMP

- **Language:** Java
- **Dependencies:**
  - Java Development Kit (JDK) 8
- **Build instructions:**
  
  ```sh
  conda create -n env_promp openjdk=8
  cd ProMP
  chmod +x ./generate.sh
  ```
  
  Note: You can change the name of the conda environment from `env_promp` to any name you prefer.
  
  **IMPORTANT:** Remember to fill in the missing data in the `generate.sh` script.
  
- **Execution command:**
  ```sh
  ./generate.sh
  ```


### GeneticAlgorithm

- **Language:** Java
- **Dependencies:**
  - Java Development Kit (JDK) 8
- **Build instructions:**
  
  ```sh
  conda create -n env_genetic_algorithm openjdk=8
  cd ProMP
  chmod +x ./generate.sh
  ```
  
  Note: You can change the name of the conda environment from `env_genetic_algorithm` to any name you prefer.
  
  **IMPORTANT:** Remember to fill in the missing data in the `generate.sh` script.
  
- **Execution command:**
  ```sh
  ./generate.sh
  ```

## Citation

If you use this repository in your research, please cite our paper:

**Paper Title:** 'From Traditional Methods to GPT-based Models for 2D Video Game Level Procedural Content Generation: An Empirical Study'

**Authors:** Daniel Cerezo, Isaac Triguero

BibTeX citation:
