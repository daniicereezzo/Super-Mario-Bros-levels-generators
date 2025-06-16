from __future__ import print_function
import argparse
import random
import os
import sys
import numpy as np
from time import perf_counter_ns

import torch
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim as optim
import torch.utils.data
from torch.autograd import Variable

import models.dcgan as dcgan
import json

def make_dir(dir_name):
    try:
        os.mkdir(dir_name)
        print(f"Directory '{dir_name}' created successfully.")
    except FileExistsError:
        print(f"WARNING: Directory '{dir_name}' already exists.")
    except PermissionError:
        print(f"ERROR: Permission denied: Unable to create '{dir_name}'.")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

parser = argparse.ArgumentParser()
parser.add_argument('--nz', type=int, default=32, help='size of the latent z vector')
parser.add_argument('--ngf', type=int, default=64)
parser.add_argument('--ndf', type=int, default=64)
parser.add_argument('--batchSize', type=int, default=32, help='input batch size')
parser.add_argument('--niter', type=int, default=5000, help='number of epochs to train for')
parser.add_argument('--lrD', type=float, default=0.00005, help='learning rate for Critic, default=0.00005')
parser.add_argument('--lrG', type=float, default=0.00005, help='learning rate for Generator, default=0.00005')
parser.add_argument('--beta1', type=float, default=0.5, help='beta1 for adam. default=0.5')
parser.add_argument('--cuda', action='store_true', help='enables cuda')
parser.add_argument('--ngpu', type=int, default=1, help='number of GPUs to use')
parser.add_argument('--netG', default='', help="path to netG (to continue training)")
parser.add_argument('--netD', default='', help="path to netD (to continue training)")
parser.add_argument('--clamp_lower', type=float, default=-0.01)
parser.add_argument('--clamp_upper', type=float, default=0.01)
parser.add_argument('--Diters', type=int, default=5, help='number of D iters per each G iter')
parser.add_argument('--n_extra_layers', type=int, default=0, help='Number of extra layers on gen and disc')
parser.add_argument('--adam', action='store_true', help='Whether to use adam (default is rmsprop)')

parser.add_argument('--seed', type=int, required=True, help='Manual seed for reproducibility')
opt = parser.parse_args()

# Create the output directory
output_folder = "samples"
make_dir(output_folder)

# Set the training_data_file
examplesJson = "training_data/example.json"

# Record the starting time
start_time = perf_counter_ns()

# Set manual seed
random.seed(opt.seed)
torch.manual_seed(opt.seed)

# Set benchmark to True for faster training
cudnn.benchmark = True

# Advise user to use CUDA if available
if torch.cuda.is_available() and not opt.cuda:
    print("WARNING: You have a CUDA device, so you should probably run with --cuda")

# Set generated image size
map_size = 32

# Load raw training data
X = np.array(json.load(open(examplesJson)))

# Number of different tile types
z_dims = 10

# Number of batches (each batch will consist of <batchsize> samples, so num_batches = num_samples / batch_size)
num_batches = X.shape[0] / opt.batchSize

# Get the values from X that are outside the limits
out_of_bounds_values = X[(X < 0) | (X >= z_dims)]
print("Values outside the limits:", out_of_bounds_values)

# One-hot encode the raw training data
print ("SHAPE ",X.shape)           #(173, 14, 28)
X = np.clip(X, 0, z_dims-1)
X_onehot = np.eye(z_dims, dtype='uint8')[X]
print ("SHAPE ",X_onehot.shape)    #(173, 14, 28, 10)
X_onehot = np.rollaxis(X_onehot, 3, 1)
print ("SHAPE ",X_onehot.shape)    #(173, 10, 28, 14)

# Create training data tensor with shape (num_samples, num_tile_types, map_size, map_size) initialized to zeros
X_train = np.zeros((X.shape[0], z_dims, map_size, map_size))

# Mark all tiles as empty
X_train[:, 2, :, :] = 1.0 

# Fill in the one-hot encoded training data
X_train[:X.shape[0], :, :X.shape[1], :X.shape[2]] = X_onehot

# Set hyperparameters
ngpu = int(opt.ngpu)
nz = int(opt.nz)
ngf = int(opt.ngf)
ndf = int(opt.ndf)
n_extra_layers = int(opt.n_extra_layers)

# Custom weights initialization called on netG and netD
def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        m.weight.data.normal_(0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.fill_(0)

netG = dcgan.DCGAN_G(map_size, nz, z_dims, ngf, ngpu, n_extra_layers)

netG.apply(weights_init)
if opt.netG != '': # load checkpoint if needed
    netG.load_state_dict(torch.load(opt.netG))
print(netG)

netD = dcgan.DCGAN_D(map_size, nz, z_dims, ndf, ngpu, n_extra_layers)
netD.apply(weights_init)

if opt.netD != '':
    netD.load_state_dict(torch.load(opt.netD))
print(netD)

input = torch.FloatTensor(opt.batchSize, z_dims, map_size, map_size)
noise = torch.FloatTensor(opt.batchSize, nz, 1, 1)
fixed_noise = torch.FloatTensor(opt.batchSize, nz, 1, 1).normal_(0, 1)
one = torch.FloatTensor([1])
mone = one * -1

if opt.cuda:
    netD.cuda()
    netG.cuda()
    input = input.cuda()
    one, mone = one.cuda(), mone.cuda()
    noise, fixed_noise = noise.cuda(), fixed_noise.cuda()

# Setup optimizer
if opt.adam:
    optimizerD = optim.Adam(netD.parameters(), lr=opt.lrD, betas=(opt.beta1, 0.999))
    optimizerG = optim.Adam(netG.parameters(), lr=opt.lrG, betas=(opt.beta1, 0.999))
    print("Using ADAM")
else:
    optimizerD = optim.RMSprop(netD.parameters(), lr = opt.lrD)
    optimizerG = optim.RMSprop(netG.parameters(), lr = opt.lrG)

gen_iterations = 0
for epoch in range(opt.niter):
    # Randomly shuffle the training data
    X_train = X_train[torch.randperm(len(X_train))]

    i = 0
    while i < num_batches:
        ############################
        # (1) Update D network
        ###########################
        for p in netD.parameters(): # Reset requires_grad
            p.requires_grad = True  # They are set to False below in netG update

        # Train the discriminator Diters times (100 if first 25 generator iterations, opt.Diters otherwise)
        if gen_iterations < 25 or gen_iterations % 500 == 0:
            Diters = 100
        else:
            Diters = opt.Diters

        j = 0
        while j < Diters and i < num_batches:
            j += 1

            # Clamp parameters to a cube
            for p in netD.parameters():
                p.data.clamp_(opt.clamp_lower, opt.clamp_upper)

            # Take a batch of real data samples
            data = X_train[i*opt.batchSize:(i+1)*opt.batchSize]

            i += 1

            # Convert the real data to a torch tensor
            real_cpu = torch.FloatTensor(data)

            # Reset gradients in the discriminator
            netD.zero_grad()

            if opt.cuda:
                real_cpu = real_cpu.cuda()

            # Copy the real data to the input tensor and create a torch Variable
            input.resize_as_(real_cpu).copy_(real_cpu)
            inputv = Variable(input)

            # Calculate the output of the discriminator on the real data
            errD_real = netD(inputv)

            # Calculate the gradients for the real data
            errD_real.backward(one)

            # Sample random noise
            noise.resize_(opt.batchSize, nz, 1, 1).normal_(0, 1)

            # Generate fake data
            with torch.no_grad(): # Avoid backpropagation
                noisev = Variable(noise) 
                fake = Variable(netG(noisev).data)
            inputv = fake

            # Calculate the output of the discriminator on the fake data
            errD_fake = netD(inputv)

            # Calculate the gradients for the fake data
            errD_fake.backward(mone)

            # Calculate the error of the discriminator
            errD = errD_real - errD_fake

            # Update the discriminator
            optimizerD.step()

        ############################
        # (2) Update G network
        ###########################
        for p in netD.parameters():
            p.requires_grad = False # Freeze the discriminator
        
        # Reset gradients in the generator
        netG.zero_grad()

        # Sample random noise
        noise.resize_(opt.batchSize, nz, 1, 1).normal_(0, 1)
        noisev = Variable(noise)

        # Generate fake data
        fake = netG(noisev)

        # Calculate the output of the discriminator on the fake data
        errG = netD(fake)

        # Calculate the error of the generator
        errG.backward(one)

        # Update the generator
        optimizerG.step()

        # Increment the generator iteration counter
        gen_iterations += 1
        
        # Print the loss every 50 iterations of the generator
        if gen_iterations % 50 == 0:
            print('[%d/%d][%d/%d][%d] Loss_D: %f Loss_G: %f Loss_D_real: %f Loss_D_fake %f'
            % (epoch, opt.niter, i, num_batches, gen_iterations,
            errD.data[0], errG.data[0], errD_real.data[0], errD_fake.data[0]))

# Store final models
torch.save(netG.state_dict(), '{0}/netG_epoch_{1}.pth'.format(output_folder, opt.niter))
torch.save(netD.state_dict(), '{0}/netD_epoch_{1}.pth'.format(output_folder, opt.niter))

# Record the ending time
end_time = perf_counter_ns()

# Print the total time taken
print(f"Total time taken: {(end_time - start_time) / 1e9} seconds")

# Append the total time taken to the output file
with open(f"{output_folder}/training_time.txt", "a") as f:
    f.write(end_time - start_time, "\n")