# This generator program expands a low-dimentional latent vector into a 2D array of tiles.
# Each line of input should be an array of z vectors (which are themselves arrays of floats -1 to 1)
# Each line of output is an array of 32 levels (which are arrays-of-arrays of integer tile ids)

import torch
from torch.autograd import Variable

import argparse
import numpy
import random
import json
from time import perf_counter_ns

import models.dcgan as dcgan
from utils.utils import *
from utils.tiles import *
from utils.repair import repair_level
    
parser = argparse.ArgumentParser()
parser.add_argument('--version', type=int, required=True, help='Level examples')
parser.add_argument('--seed', type=int, required=True, help='Manual seed for reproducibility')
parser.add_argument('--n_levels', type=int, default=200, help='Number of levels to generate')
args = parser.parse_args()

# Create the output directory and set the generator model to load based on the version
if args.version == 1:
    non_repaired_levels_folder = f"levels_CorrectedGAN_v1"
    repaired_levels_folder = f"levels_CorrectedGAN_v1_repaired"
    modelToLoad = "samples_v1/netG_epoch_5000.pth"
elif args.version == 2:
    non_repaired_levels_folder = f"levels_CorrectedGAN_v2"
    repaired_levels_folder = f"levels_CorrectedGAN_v2_repaired"
    modelToLoad = "samples_v2/netG_epoch_5000.pth"
else:
    print("Invalid model version. Please choose 1 (only trained on level 1-1) or 2 (trained on all levels).")
    sys.exit(1)

# Set the seed
random.seed(args.seed)
torch.manual_seed(args.seed)

# Create the default levels folder
make_dir(non_repaired_levels_folder)
make_dir(repaired_levels_folder)

# Set the hyperparameters
nz = 32
imageSize = 32
ngf = 64
ngpu = 1
n_extra_layers = 0
z_dims = 13
n_scenes_per_level = 5

# Load the generator
generator = dcgan.DCGAN_G(imageSize, nz, z_dims, ngf, ngpu, n_extra_layers)
generator.load_state_dict(torch.load(modelToLoad, map_location=lambda storage, loc: storage))

def generate_random_level():
    # Generate random latent vectors
    input = []
    for j in range(n_scenes_per_level):
        input.append([random.uniform(-1, 1) for _ in range(nz)])
    input = numpy.array(input)
    latent_vector = torch.FloatTensor(input).view(n_scenes_per_level, nz, 1, 1)

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

# Generate the levels
for i in range(args.n_levels):
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
    level = generate_random_level()
    
    # Record the end time
    end_time = perf_counter_ns()

    # Save the non-repaired level
    print(f"Saving non-repaired level_{i}.txt")
    with open(f"{non_repaired_levels_folder}/level{i}.txt", "w") as f:
        f.write(level)
    
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