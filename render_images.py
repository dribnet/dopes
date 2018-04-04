import argparse
import glob
import sys
import os
import numpy as np
from classloader import load_image_function
import random
import io
from PIL import Image

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="run vgg16")
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
    parser.add_argument('--length', default=24, type=int,
                        help='Length of generated vector list')
    args = parser.parse_args()

    array_to_image = load_image_function(args.image_function)    

    if args.random_seed:
      print("Setting random seed: ", args.random_seed)
      random.seed(args.random_seed)
      np.random.seed(args.random_seed)
      for i in range(args.random_seed):
        n = np.random.uniform()

    if args.input_glob is None:
        rand_array = np.random.uniform(low=0.02, high=0.98, size=(args.length, 8))
        im = array_to_image(rand_array, args.size)
        im.save(args.outfile)
        print("rand -> {}".format(args.outfile))
        sys.exit(0)

    files = sorted(glob.glob(args.input_glob))
    print("Found {} files in glob {}".format(len(files), args.input_glob))
    if len(files) == 0:
        print("No files to process")
        sys.exit(0)

    for infile in files:
        best_array = np.load(infile)
        im = array_to_image(best_array, args.size)
        if args.outfile is not None:
            outfile = args.outfile
        else:
            dirname = os.path.dirname(infile)
            outfile = os.path.join(dirname, args.outbase)

        im.save(outfile)
        print("{:7s} -> {}".format(infile, outfile))
    
