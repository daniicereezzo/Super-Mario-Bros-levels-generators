import torch
from torch.autograd import Variable

import argparse
import numpy
import random
import json
from time import perf_counter_ns

import models.dcgan as dcgan

import cma

from utils.tiles import *
from utils.utils import *
from utils.repair import repair_level
from fitness_functions import get_fitness_functions
    
parser = argparse.ArgumentParser()
parser.add_argument('--seed', type=int, required=True, help='Seed for reproducibility')
parser.add_argument('--n_levels', type=int, default=200, help='Number of levels to generate')
args = parser.parse_args()

# Set the generator model to load
modelToLoad = "samples/netG_epoch_5000.pth"

random.seed(args.seed)
torch.manual_seed(args.seed)

# Create the levels folders
non_repaired_levels_folder = f"levels_MarioGAN"
repaired_levels_folder = f"levels_MarioGAN_repaired"
make_dir(non_repaired_levels_folder)
make_dir(repaired_levels_folder)

# Set the hyperparameters
nz = 32
imageSize = 32
ngf = 64
ngpu = 1
n_extra_layers = 0
z_dims = 10
n_scenes_per_level = 5

# Load the generator
generator = dcgan.DCGAN_G(imageSize, nz, z_dims, ngf, ngpu, n_extra_layers)
generator.load_state_dict(torch.load(modelToLoad, map_location=lambda storage, loc: storage))

def generate_cma_level(fitness_function):
    # Initialize search algorithm
    es = cma.CMAEvolutionStrategy(n_scenes_per_level * nz * [0], 0.5, {'seed': seed})

    #cma.CMAEvolutionStrategy(4 * [1], 1, {'seed':234})
    #'BoundaryHandler': 'BoundTransform  # or BoundPenalty, unused when ``bounds in (None, [None, None])``',
    #'bounds': '[None, None]  # lower (=bounds[0]) and upper domain boundaries, each a scalar or a list/vector',
    
    # Run the search algorithm
    es.optimize(fitness_function)

    # Get best individual
    best = numpy.array(es.best.get()[0])
    print("Best: ", best)
    print("Fitness: ", fitness_function(best))
    latent_vector = torch.FloatTensor(best).view(n_scenes_per_level, nz, 1, 1)

    # Generate scenes
    with torch.no_grad():
        levels = generator(Variable(latent_vector))

    # Crop each scene to 14x28
    level = levels.data.cpu().numpy()
    level = level[:, :, :14, :28]

    # Convert from one-hot format to integer
    level = numpy.argmax(level, axis=1)

    # Combine scenes into a single level and convert to VGLC format
    level = level.tolist()
    combined_level = []
    for _ in range(len(level[0])):
        combined_level.append("")
    for scene in level:
        for k, row in enumerate(scene):
            new_row = "".join([from_int_to_vglc(tile) for tile in row])
            combined_level[k] += new_row
    return "\n".join(combined_level)

# Create the times and seeds lists
generation_times = []
repair_times = []
seeds = []

# Select only the fitness functions associated with tiles MarioGAN understands (from 0 to 9 + gan_fitness_function)
fitness_functions = get_fitness_functions(generator, n_scenes_per_level, nz)[:11]

# Set the number of times each fitness function is selected
n_fitness_functions = args.n_levels // len(fitness_functions)

# Set the iteration from which the fitness functions are randomly selected
limit_iteration = n_fitness_functions * len(fitness_functions)

# Generate the levels
for i in range(args.n_levels):
    # Select a fitness function
    if i < limit_iteration:     # This is to ensure that the calls to the fitness functions are as balanced as possible
        fitness_function = fitness_functions[i % len(fitness_functions)]
    else:
        fitness_function = random.choice(fitness_functions)

    # Create the seed
    seed = random.randint(0, 2**32 - 1)

    # Record the seed
    seeds.append(seed)

    # Set the seed
    random.seed(seed)
    torch.manual_seed(seed)

    # Record the start time
    start_time = perf_counter_ns()

    # Generate the level
    level = generate_cma_level(fitness_function)
    
    # Record the end time
    end_time = perf_counter_ns()

    # Save the non-repaired level
    print(f"Saving non-repaired level_{i}.txt")
    with open(f"{non_repaired_levels_folder}/level{i}.txt", "w") as f:
        f.write(level)
    
    cma.plot()
    
    # Record the generation time
    generation_time = end_time - start_time
    generation_times.append(generation_time)

    # Record the start time for the repair
    start_time = perf_counter_ns()

    # Repair the level
    repaired_level = repair_level(level.splitlines())
    
    # Record the end time for the repair
    end_time = perf_counter_ns()

    # Save the repaired level
    print(f"Saving level_{i}.txt")
    with open(f"{repaired_levels_folder}/level{i}.txt", "w") as f:
        f.write(repaired_level)

    # Record the repair time
    repair_time = end_time - start_time
    repair_times.append(repair_time)

# Save non-repaired levels times and seeds
with open(f"{non_repaired_levels_folder}/times.json", "w") as f:
    json.dump(generation_times, f, indent=4)

with open(f"{non_repaired_levels_folder}/seeds.json", "w") as f:
    json.dump(seeds, f, indent=4)

# Save repaired levels times and seeds
with open(f"{repaired_levels_folder}/times.json", "w") as f:
    json.dump([generation_time + repair_time for generation_time, repair_time in zip(generation_times, repair_times)], f, indent=4)

with open(f"{repaired_levels_folder}/seeds.json", "w") as f:
    json.dump(seeds, f, indent=4)