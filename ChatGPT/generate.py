from time import perf_counter_ns
import os
import random
import json
import argparse
from dotenv import load_dotenv

from openai import OpenAI
from utils.repair import *

def request_chat_completion(client, system_prompt, user_prompts, temperature, seed):
    messages = [{"role": "system", "content": system_prompt}]

    for user_prompt in user_prompts:
        messages.append({"role": "user", "content": user_prompt})

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=temperature,
            seed=seed,
        )

        answer = completion.choices[0].message.content

        print(answer)

        messages.append({"role": "assistant", "content": answer})

    return answer

parser = argparse.ArgumentParser()
parser.add_argument('--seed', type=int, required=True, help='Seed for reproducibility')
parser.add_argument('--n_levels', type=int, default=200, help='Number of levels to generate')
args = parser.parse_args()

random.seed(args.seed)

levels_per_batch = 5        # If you want to change this, you must also change the prompts so ChatGPT generates the correct number of levels per API call
n_batches = args.n_levels // levels_per_batch if args.n_levels % levels_per_batch == 0 else args.n_levels // levels_per_batch + 1

possible_temperatures = [0.8, 0.9, 1.0]

# Set up OpenAI client
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(
  api_key=api_key
)

# Read the prompts
prompts_folder = "prompts"

with open(f"{prompts_folder}/system_prompt.txt", "r") as f:
    system_prompt = f.read()

with open(f"{prompts_folder}/repair_pipes_prompt.txt", "r") as f:
    repair_pipes_prompt = f.read()

'''with open(f"{prompts_folder}/repair_size_prompt.txt", "r") as f:
    repair_pipes_prompt = f.read()
    f.close()'''

with open(f"{prompts_folder}/user_prompt.txt", "r") as f:
    user_prompt = f.read()

with open(f"{prompts_folder}/user_prompt_2.txt", "r") as f:
    user_prompt_2 = f.read()

user_prompts = [user_prompt, user_prompt_2]

for temp in possible_temperatures:
    generation_times = []
    repair_times = []
    seeds = []

    # Make levels folder
    non_repaired_levels_folder = f"levels_ChatGPT_{temp}"
    os.makedirs(non_repaired_levels_folder, exist_ok=True)

    # Make subfolder for repaired levels
    repaired_levels_folder = f"{non_repaired_levels_folder}_repaired"
    os.makedirs(repaired_levels_folder, exist_ok=True)

    for n in range(n_batches):
        print(f"Generating batch {n}...")

        seed = random.randint(0, 2**32 - 1)

        # Repeat if any error occurs
        while(True):
            try:
                start_time = perf_counter_ns()

                levels_json = request_chat_completion(client, system_prompt, user_prompts, temp, seed)
                levels_json = levels_json.split("```json")[1].split("```")[0]
                levels = json.loads(levels_json)

                '''pipe_adjusted_levels = []
                for level in levels:
                    pipe_adjusted_level = request_chat_completion(client, repair_pipes_prompt, ["\n".join(level), "Remove everything from the previous message but the final generated level and return it as a JSON list."], 0, seed)
                    pipe_adjusted_level = "\n".join(pipe_adjusted_level.split("\n")[1:-1])
                    pipe_adjusted_levels.append(json.loads(pipe_adjusted_level))'''
                
                final_levels = []
                for level in levels:
                    final_levels.append(repair_level_size(level))

                end_time = perf_counter_ns()

                # Check that it has generated the correct number of levels
                if len(final_levels) != levels_per_batch:
                    print(f"Error: Expected {levels_per_batch} levels, but got {len(final_levels)}")
                    continue

                # save levels to a file
                for i, level in enumerate(final_levels):
                    print(f"Saving non-repaired level{n * levels_per_batch + i}.txt")
                    with open(f"{non_repaired_levels_folder}/level{n * levels_per_batch + i}.txt", "w") as f:
                        f.write(level)

                # save times and seeds
                generation_time_per_level = (end_time - start_time) / levels_per_batch
                for i in range(levels_per_batch):
                    generation_times.append(generation_time_per_level)
                    seeds.append(seed)

                start_time = perf_counter_ns()

                # repair levels
                repaired_levels = [repair_level(level.splitlines()) for level in final_levels]

                end_time = perf_counter_ns()

                # save repaired levels to a file
                for i, level in enumerate(repaired_levels):
                    print(f"Saving repaired level{n * levels_per_batch + i}.txt")
                    with open(f"{repaired_levels_folder}/level{n * levels_per_batch + i}.txt", "w") as f:
                        f.write(level)

                # save times
                repair_time_per_level = (end_time - start_time) / levels_per_batch
                for i in range(levels_per_batch):
                    repair_times.append(repair_time_per_level)
                     
            except Exception as e:
                print(f"Error: {e}")
                continue

            break 

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