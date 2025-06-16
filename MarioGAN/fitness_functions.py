import torch
from torch.autograd import Variable

import sys
import os
import argparse
import numpy
import random
import json
import math
from time import perf_counter_ns

import models.dcgan as dcgan
from utils.tiles import *

# Define the fitness functions
def fitness_maximize_tile_type(x, tile_type, generator, n_scenes_per_level, nz):
    x = numpy.array(x)
    latent_vector = torch.FloatTensor(x).view(n_scenes_per_level, nz, 1, 1)
    with torch.no_grad():
        levels = generator(Variable(latent_vector))

    levels.data = levels.data[:, :, :14, :28]
    im = levels.data.cpu().numpy()
    im = numpy.argmax(im, axis = 1)

    num_tiles = (len(im[im == from_vglc_to_int(tile_type)]))
    return 100.0 - num_tiles

def gan_fitness_function(x, generator, n_scenes_per_level, nz):
    x = numpy.array(x)

    latent_vector = torch.FloatTensor(x).view(n_scenes_per_level, nz, 1, 1)
    with torch.no_grad():
        levels = generator(Variable(latent_vector))
    levels.data = levels.data[:, :, :14, :28]

    return solid_blocks_fraction(levels.data, 0.4) * ground_blocks_fraction(levels.data, 0.8)

def ground_blocks_fraction(data, frac):
    ground_count = (data[:, from_vglc_to_int(GROUND), 13, :] > 0).sum()
    return math.sqrt(math.pow(ground_count - frac*28, 2))

def solid_blocks_fraction(data, frac):      # COMPROBAR QUE ESTO ESTÁ BIEN
    solid_block_count = (data[:, :from_vglc_to_int(EMPTY), :, :] > 0).sum() + (data[:, (from_vglc_to_int(EMPTY) + 1):, :, :] > 0).sum()
    return math.sqrt(math.pow(solid_block_count - frac*14*28, 2))

def get_fitness_functions(generator, n_scenes_per_level, nz):
    fitness_functions = [lambda x : gan_fitness_function(x, generator, n_scenes_per_level, nz)]
    fitness_functions.extend([lambda x : fitness_maximize_tile_type(x, tile_type, generator, n_scenes_per_level, nz) for tile_type in TILES])

    return fitness_functions