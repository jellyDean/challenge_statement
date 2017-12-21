import tables
import numpy as np
from PIL import Image
# https://stackoverflow.com/questions/2659312/how-do-i-convert-a-numpy-array-to-and-display-an-image
# https://stackoverflow.com/questions/3636344/read-flat-list-into-multidimensional-array-matrix-in-python


def read_and_shape_input_data(file_path, matrix_height, matrix_width):

    with tables.open_file(file_path) as infile:

        # TODO: do a check that length and timestamps is 65536 if they arent error out and an exception too
        # convert to numpy array to make life easier. could also use modulus and build manually
        timestamp_matrix = np.array(infile.root.time).reshape((matrix_height, matrix_width))
        count_matrix = np.array(infile.root.counts).reshape((matrix_height, matrix_width))

    return timestamp_matrix, count_matrix

# create a matrix RRGB canvas with all 0's initially
def main():
    input_data_location = '/Users/deanhutton/workdir/Personal/Repos/challenge_statement/sample_data.inp'
    matrix_width, matrix_height = 256, 256

    # Create a blank 256x256 canvas with all RGB values zeroed out
    black_matrix = np.zeros((matrix_height, matrix_width, 3), dtype=np.uint8)
    rgb_matrix = np.zeros((matrix_height, matrix_width, 3), dtype=np.uint8)

    timestamp_matrix, count_matrix = read_and_shape_input_data(input_data_location, matrix_height, matrix_width)

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

if __name__ == "__main__":
    # execute only if run as a script
    main()