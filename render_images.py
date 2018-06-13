import argparse
import glob
import sys
import os
import numpy as np
from classloader import load_image_function
from braceexpand import braceexpand
import random
import io
from PIL import Image

def real_glob(rglob):
    glob_list = braceexpand(rglob)
    files = []
    for g in glob_list:
        files = files + glob.glob(g)
    return sorted(files)

def save_file_or_files(infile, im, outfile):
    # allow list of outputs (layers)
    if isinstance(im, list):
        for ix in range(len(im)):
            outfile_name = outfile.format(ix+1)
            im[ix].save(outfile_name)
            print("{:7s} -> {}".format(infile, outfile_name))
    else:
        im.save(outfile)
        print("{:7s} -> {}".format(infile, outfile))

def lerp(val, low, high):
    """Linear interpolation"""
    return low + (high - low) * val

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="render dopes image")
    parser.add_argument('--input-glob', default=None,
                        help="inputs")
    parser.add_argument('--outfile', default=None,
                        help="single output file")
    parser.add_argument('--outbase', default="best_1200_redo.png", 
                         help='basename for the output file')
    parser.add_argument('--image-function', default='renderer.lines_bgcolor.array_to_image',
                        help="(none)")
    parser.add_argument('--size', default=1200, type=int,
                        help='(none)')
    parser.add_argument('--random-seed', default=None, type=int,
                        help='Use a specific random seed (for repeatability)')
    parser.add_argument('--interpolate', default=None, type=int,
                        help='Turn on interpolation and give a number of frames of output')
    parser.add_argument('--versions', default=1, type=int,
                        help='how many versions to make [put formatter in filename if > 1]')
    parser.add_argument('--length', default=None, type=int,
                        help='Length of generated vector list')
    args = parser.parse_args()

    array_to_image = load_image_function(args.image_function)    

    if args.random_seed:
      print("Setting random seed: ", args.random_seed)
      random.seed(args.random_seed)
      np.random.seed(args.random_seed)
      # for i in range(args.random_seed):
      #   n = np.random.uniform()

    if args.input_glob is None:
        files = ["(random)"]
    else:
        files = real_glob(args.input_glob)
        print("Found {} files in glob {}".format(len(files), args.input_glob))
        if len(files) == 0:
            print("No files to process")
            sys.exit(0)

    if args.interpolate is not None:
        if len(files) != 2:        
            print("Interpolate is brittle and needs exactly two files")
            sys.exit(0)
        input_array1 = np.load(files[0])
        print("Loaded {}: shape {}".format(files[0], input_array1.shape))
        input_array2 = np.load(files[1])
        print("Loaded {}: shape {}".format(files[1], input_array2.shape))
        if len(input_array1) != len(input_array2):
            print("Interpolate is brittle and files are not equal length: {}, {}".format(len(input_array1), len(input_array2)))
            sys.exit(0)
        for i in range(args.interpolate):
            frac = i / (args.interpolate - 1)
            interp_array = lerp(frac, input_array1, input_array2)
            im = array_to_image(interp_array, args.size)
            outfile = args.outfile.format(i+1)
            save_file_or_files("interpolation {}".format(i+1), im, outfile)
        sys.exit(0)

    cur_file_num = 1
    for infile in files:
        if infile == "(random)":
            if args.length is None:
                length = 24
            else:
                length = args.length
            input_array = np.random.uniform(low=0.02, high=0.98, size=(length, 8))
            print("Created random input with shape {}".format(input_array.shape))
        else:
            input_array = np.load(infile)
            print("Loaded {}: shape {}".format(infile, input_array.shape))
            if args.length is not None:
                input_array = input_array[:args.length]

        for n in range(args.versions):
            im = array_to_image(input_array, args.size)
            if args.outfile is not None:
                outfile = args.outfile
            else:
                dirname = os.path.dirname(infile)
                outfile = os.path.join(dirname, args.outbase)

            # somewhat messy handling of list case twice for file naming
            if not isinstance(im, list):
                outfile = outfile.format(cur_file_num)
                cur_file_num = cur_file_num + 1
            save_file_or_files(infile, im, outfile)
