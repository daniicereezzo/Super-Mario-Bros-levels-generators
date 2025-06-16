# Super Mario Bros levels generators

## Overview

Repository containing the Super Mario Bros levels generators evaluated in the Bachelor Thesis **'Evolución de las técnicas de Generación Automática de Niveles en Videojuegos: De algoritmos tradicionales a modelos avanzados de Deep Learning'**.

Each generator contains its own source code in the subfolder identified by its name and has its own specific build and execution instructions.

This README provides some guidelines on how to build and run each project.

## Prerequisites

Make sure you have installed a conda distribution before building and running any project.

## General guidelines

Every generator in this repository follows a similar build process:

1. Create a conda environment for that generator.
2. If more dependencies are needed:
 - Activate the environment.
 - Install the generator dependencies (following the specific instructions for each generator).
 - Deactivate the environment.
3. Navigate to the generator subfolder:
4. Complete the `generate.sh` script with the following data:
 - Path of your conda distribution.
 - Name of the environment you created.
 - Seed you want to use for reproducibility.
 - Number of levels you want to generate.
5. Execute the `generate.sh` script to generate the levels.
