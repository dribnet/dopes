A simple rendering system to get started.

Instructions: make a copy of linesys1.py and try your own stuff.

Here are sample commands which generate random images using the
drawing system provided in "linesys1". After running these commands,
compare the output files and notice that there are two of each
time of image at different sizes (eg: the scaling is working well).

```bash
# these two should match when scaled
python render_images.py \
  --image-function linesys1.array_to_image \
  --random-seed 3 \
  --size 1200 \
  --outfile outputs/linesys1_s1200_r03.png

python render_images.py \
  --image-function linesys1.array_to_image \
  --random-seed 3 \
  --size 600 \
  --outfile outputs/linesys1_s600_r03.png

# these two should also match
python render_images.py \
  --image-function linesys1.array_to_image \
  --length 12 \
  --random-seed 4 \
  --outfile outputs/linesys1_l12_r04.png

python render_images.py \
  --image-function linesys1.array_to_image \
  --length 12 \
  --random-seed 4 \
  --size 1024 \
  --outfile outputs/linesys1_l12_s1024_r04.png

# and these two
python render_images.py \
  --image-function linesys1.array_to_image \
  --length 60 \
  --random-seed 5 \
  --size 200 \
  --outfile outputs/linesys1_l60_s200_rand_05.png

python render_images.py \
  --image-function linesys1.array_to_image \
  --length 60 \
  --random-seed 5 \
  --size 600 \
  --outfile outputs/linesys1_l60_s600_rand_05.png

```
