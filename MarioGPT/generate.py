from mario_gpt import MarioLM, SampleOutput
from time import perf_counter_ns
import os
import sys
import random
import json
import torch
import argparse

from utils.repair import *

parser = argparse.ArgumentParser()
parser.add_argument('--seed', type=int, required=True, help='Seed for reproducibility')
parser.add_argument('--n_levels', type=int, default=200, help='Number of levels to generate')
args = parser.parse_args()

torch.manual_seed(args.seed)
random.seed(args.seed)

# pretrained_model = shyamsn97/Mario-GPT2-700-context-length

mario_lm = MarioLM()

# use cuda to speed stuff up
# import torch
#if torch.cuda.is_available():
#    device = torch.device('cuda')
#    mario_lm = mario_lm.to(device)

pipe_options = ["no", "little", "some", "many", "number"]
enemy_options = ["no", "little", "some", "many", "number"]
block_options = ["little", "some", "many", "number"]
elevation_options = ["low", "high"]

all_combinations = []
for pipe in pipe_options:
    for enemy in enemy_options:
        for block in block_options:
            for elevation in elevation_options:
                all_combinations.append((pipe, enemy, block, elevation))

possible_temperatures = [2.0, 2.4]

# Create the times and seeds lists
generation_times = []
seeds = []
repair_times = []

not_random_iterations = (args.n_levels // len(all_combinations)) * len(all_combinations)

for temp in possible_temperatures:
    # Make levels folder
    non_repaired_levels_folder = f"levels_MarioGPT_no_cuda_{temp}"
    os.makedirs(non_repaired_levels_folder, exist_ok=True)

    # Make repaired levels folder
    repaired_levels_folder = f"levels_MarioGPT_no_cuda_{temp}_repaired"
    os.makedirs(repaired_levels_folder, exist_ok=True)

    for n in range(args.n_levels):
        if n < not_random_iterations:   # This is to ensure that the usage of the prompts is as balanced as possible
            pipe, enemy, block, elevation = all_combinations[n % len(all_combinations)]
        else:
            pipe = random.choice(pipe_options)
            enemy = random.choice(enemy_options)
            block = random.choice(block_options)
            elevation = random.choice(elevation_options)

        if pipe == "number":
            pipe = random.randint(0, 1000)
        if enemy == "number":
            enemy = random.randint(0, 1000)
        if block == "number":
            block = random.randint(0, 1000)

        prompts = [f"{pipe} pipes, {enemy} enemies, {block} blocks, {elevation} elevation"]

        print(f"Generating level_t_{temp}_p_{pipe}_e_{enemy}_b_{block}_h_{elevation}_n_{n}")

        seed = random.randint(0, 2**32 - 1)

        torch.manual_seed(seed)
        random.seed(seed)

        start_time = perf_counter_ns()

        generated_level = mario_lm.sample(
            prompts=prompts,
            num_steps=1960,                 # 1960 = 140 x 14 (width x height)
            temperature=temp,
            use_tqdm=True,
        )

        end_time = perf_counter_ns()

        # save image
        #generated_level.img.save(f"level_p_{pipe}_e_{enemy}_b_{block}_h_{elevation}_n_{n}.png")

        # save text level to file
        generated_level.save(f"{non_repaired_levels_folder}/level_p_{pipe}_e_{enemy}_b_{block}_h_{elevation}_n_{n}.txt")

        generation_times.append(end_time - start_time)
        seeds.append(seed)

        start_time = perf_counter_ns()

        # repair level
        repaired_level = repair_level(generated_level.level)

        end_time = perf_counter_ns()

        # save repaired level to a file
        with open(f"{repaired_levels_folder}/level_p_{pipe}_e_{enemy}_b_{block}_h_{elevation}_n_{n}_repaired.txt", "w") as f:
            f.write(repaired_level)
            f.close()

        repair_times.append(end_time - start_time)     

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