import tables
import numpy as np
from PIL import Image
# https://stackoverflow.com/questions/2659312/how-do-i-convert-a-numpy-array-to-and-display-an-image
# https://stackoverflow.com/questions/3636344/read-flat-list-into-multidimensional-array-matrix-in-python

input_data_location = '/Users/deanhutton/workdir/Personal/Repos/challenge_statement/sample_data.inp'

with tables.open_file(input_data_location) as infile:
    timestamps = infile.root.time
    counts = infile.root.counts

    # create a matrix RRGB canvas with all 0's initially
    w, h = 256, 256
    black_matrix = np.zeros((h, w, 3), dtype=np.uint8)
    rgb_matrix = np.zeros((h, w, 3), dtype=np.uint8)

    # TODO: do a check that length and timestamps is 65536 if they arent error out
    shape = (256, 256)

    # convert to numpy array to make life easier. could also use modulus and build manually
    timestamp_numpy_array = np.array(timestamps)
    count_numpy_array = np.array(counts)

    # reshape the array into a n x n matrix
    timestamp_matrix = timestamp_numpy_array.reshape(shape)
    count_matrix = count_numpy_array.reshape(shape)

    #Grey Scale Case
    # for i, row in enumerate(timestamp_matrix):
    #     for j, timestamps in enumerate(row):
    #         pix = [0, 0, 0]
    #         count_sum = 0
    #         for timestamp in timestamps:
    #             if 6296 <= int(timestamp) <= 6304:
    #                 count_sum = sum(count_matrix[i][j])
    #                 pix[0] = count_sum
    #                 pix[1] = count_sum
    #                 pix[2] = count_sum
    #
    #         black_matrix[i][j] = pix

    # TODO: RGB Case
    for i, row in enumerate(timestamp_matrix):
        for j, timestamps in enumerate(row):
            pix = [0, 0, 0]
            red_count_sum = 0
            green_count_sum = 0
            blue_count_sum = 0
            for timestamp in timestamps:
                timestamp_int = int(timestamp)
                if 16660 <= timestamp_int <= 16685:
                    red_count_sum = sum(count_matrix[i][j])
                elif 11994 <= timestamp_int <= 12012:
                    green_count_sum = sum(count_matrix[i][j])
                elif 15600 <= timestamp_int <= 15630:
                    blue_count_sum = sum(count_matrix[i][j])
                else:
                    continue

                pix[0] = red_count_sum
                pix[1] = green_count_sum
                pix[2] = blue_count_sum

            rgb_matrix[i][j] = pix


# img = Image.fromarray(black_matrix, 'RGB')
# img.save('greyscale.png')

img = Image.fromarray(rgb_matrix, 'RGB')
img.save('rgb.png')

# TODO: Do a check for one pixel, the length of timestamps and counts must be equal otherwise error out
# TODO: leave the with as soon as possible so file doesnt remain open

