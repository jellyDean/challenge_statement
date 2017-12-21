"""
generate_images.py
Developer: Dean Hutton
Project: Raster Image Generation
Date: 12/20/17

References:
https://stackoverflow.com/questions/2659312/how-do-i-convert-a-numpy-array-to-and-display-an-image
https://stackoverflow.com/questions/3636344/read-flat-list-into-multidimensional-array-matrix-in-python
"""


import tables
import numpy as np
from PIL import Image


def read_and_shape_input_data(file_path, matrix_height, matrix_width):
    """
    Function that reads in the input data and transforms it into a 2 256x256 matrices
    :param str file_path: The location of the input data on disk
    :param int matrix_height: The height of the output matrix
    :param int matrix_width: The width of the matrix
    :return: timestamp_matrix and count_matrix matrices that contain the data that will be processed
    :rtype: numpy_arrays
    """
    with tables.open_file(file_path) as infile:

        # TODO: do a check that length and timestamps is 65536 if they arent error out and an exception too
        # convert to numpy array to make life easier. could also use modulus and build manually
        timestamp_matrix = np.array(infile.root.time).reshape((matrix_height, matrix_width))
        count_matrix = np.array(infile.root.counts).reshape((matrix_height, matrix_width))

    return timestamp_matrix, count_matrix


def populate_grey_scale_matrix(timestamp_matrix, count_matrix, matrix_template):
    """
    Function that iterates through the matrix and checks to see if the timestamps fall within the grey ion range.
    If the ions timestamp falls within range, look up the corresponding counts for that timestamp and sum them all
    together. Lastly set the RGB to values to sum of counts for each pixel.
    :param numpy_array timestamp_matrix: The timestamps that were transformed from the input data
    :param numpy_array count_matrix: The counts that were transformed from the input data
    :param numpy_array matrix_template: The blank template that is populated and returned
    :return: The populated matrix that can be saved to disk to generate an image
    :rtype: numpy_array
    """
    for i, row in enumerate(timestamp_matrix):
        for j, timestamps in enumerate(row):
            pix = [0, 0, 0]
            for timestamp in timestamps:
                if 6296 <= int(timestamp) <= 6304:
                    count_sum = sum(count_matrix[i][j])
                    pix[0] = count_sum
                    pix[1] = count_sum
                    pix[2] = count_sum

            matrix_template[i][j] = pix

    return matrix_template


def populate_rgb_matrix(timestamp_matrix, count_matrix, matrix_template):
    """
    Function that iterates through the matrix and checks to see if the timestamps fall within the red, green and
     blue ion range. If the ions timestamp falls within range, look up the corresponding counts for that timestamp
     and sum them all together. Lastly set the RGB to values to sum of counts for each pixel.
    :param numpy_array timestamp_matrix: The timestamps that were transformed from the input data
    :param numpy_array count_matrix: The counts that were transformed from the input data
    :param numpy_array matrix_template: The blank template that is populated and returned
    :return: The populated matrix that can be saved to disk to generate an image
    :rtype: numpy_array
    """
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

            matrix_template[i][j] = pix

    return matrix_template


def export_image(rgb_matrix, output_image_location):
    """
    Function that saves the output image to disk
    :param numpy_array rgb_matrix: The populated numpy matrix
    :param str output_image_location: The location of where to save the image
    :return: Saves the image to disk
    :rtype: None
    """
    img = Image.fromarray(rgb_matrix, 'RGB')
    img.save(output_image_location)


# create a matrix RGB canvas with all 0's initially
def main():
    input_data_location = "/Users/deanhutton/workdir/Personal/Repos/challenge_statement/sample_data.inp"
    output_image_location = "/Users/deanhutton/workdir/Personal/Repos/challenge_statement/rgb.png"
    matrix_width, matrix_height = 256, 256

    # Create a blank 256x256 canvas with all RGB values zeroed out
    zeroed_out_rgb_matrix = np.zeros((matrix_height, matrix_width, 3), dtype=np.uint8)

    # Create data types needed to process
    timestamp_matrix, count_matrix = read_and_shape_input_data(input_data_location, matrix_height, matrix_width)

    # Populate the out matrix with the data types
    rgb_matrix = populate_rgb_matrix(timestamp_matrix, count_matrix, zeroed_out_rgb_matrix)

    # Save the image to disk
    export_image(rgb_matrix, output_image_location)


    # TODO: Do a check for one pixel, the length of timestamps and counts must be equal otherwise error out
    # TODO: leave the with as soon as possible so file doesnt remain open

if __name__ == "__main__":
    # execute only if run as a script
    main()
