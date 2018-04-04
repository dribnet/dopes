import sys
import math
from PIL import Image, ImageDraw
import numpy as np
import csv

# canonical interpolation function, like https://p5js.org/reference/#/p5/map
def map_number(n, start1, stop1, start2, stop2):
  return ((n-start1)/(stop1-start1))*(stop2-start2)+start2;

# input: array of real vectors, length 8, each component normalized 0-1
def array_to_image(a, size=224):
    # split input array into header and rest
    header_length = 2
    head = a[:header_length]
    rest = a[header_length:]

    # determine background color from header
    R = int(map_number(head[0][0], 0, 1, 0, 255))
    G = int(map_number(head[0][1], 0, 1, 0, 255))
    B = int(map_number(head[0][2], 0, 1, 0, 255))

    # create the image and drawing context
    im = Image.new('RGB', (size, size), (R, G, B))
    draw = ImageDraw.Draw(im, 'RGB')

    # store layer colors in list
    layer_colors = [None, None, None]

    # determine layer1 color from header
    R = int(map_number(head[0][3], 0, 1, 0, 255))
    G = int(map_number(head[0][4], 0, 1, 0, 255))
    B = int(map_number(head[0][5], 0, 1, 0, 255))
    layer_colors[0] = [R, G, B]

    # determine layer2 color from header
    R = int(map_number(head[1][0], 0, 1, 0, 255))
    G = int(map_number(head[1][1], 0, 1, 0, 255))
    B = int(map_number(head[1][2], 0, 1, 0, 255))
    layer_colors[1] = [R, G, B]

    # determine layer3 color from header
    R = int(map_number(head[1][3], 0, 1, 0, 255))
    G = int(map_number(head[1][4], 0, 1, 0, 255))
    B = int(map_number(head[1][5], 0, 1, 0, 255))
    layer_colors[2] = [R, G, B]

    # split the rest into three separate interleaved lists
    layer1_list = rest[0::3]
    layer2_list = rest[1::3]
    layer3_list = rest[2::3]

    # example of debugging:
    # print(layer_colors)

    # store those in a list
    layer_lists = [layer1_list, layer2_list, layer3_list]

    # now draw circles in each layer
    bottom_min_width = 0.02 * size
    bottom_max_width = 0.2 * size
    for layer_index in range(3):
        # make each layer smaller than the one below
        min_width = bottom_min_width / (layer_index + 1)
        max_width = bottom_max_width / (layer_index + 1)
        # choose color and list for layer
        R, G, B = layer_colors[layer_index]
        layer_list = layer_lists[layer_index]
        # draw this layer
        for e in layer_list:
            w2 = int(map_number(e[0], 0, 1, min_width, max_width))
            # line width
            w = 2 * w2 + 2
            # line position
            x1 = map_number(e[1], 0, 1, w2, size-w2)
            y1 = map_number(e[2], 0, 1, w2, size-w2)
            x2 = map_number(e[3], 0, 1, w2, size-w2)
            y2 = map_number(e[4], 0, 1, w2, size-w2)
            x3 = map_number(e[5], 0, 1, w2, size-w2)
            y3 = map_number(e[6], 0, 1, w2, size-w2)
            # draw circles
            draw.ellipse((x1-w2, y1-w2, x1+w2, y1+w2), fill=(R, G, B))
            draw.ellipse((x2-w2, y2-w2, x2+w2, y2+w2), fill=(R, G, B))
            draw.ellipse((x3-w2, y3-w2, x3+w2, y3+w2), fill=(R, G, B))

    return im

def array_to_image_hifi(a, size=564):
    return array_to_image(a, size)
