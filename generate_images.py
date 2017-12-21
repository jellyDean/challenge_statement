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
import sys
import argparse
import os
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
    try:
        # TODO: do a check that timestamp_matrix and count_matrix length is 65536 if they aren't error out
        with tables.open_file(file_path) as infile:
            # convert to numpy array to make life easier. could also use modulus and build manually
            timestamp_matrix = np.array(infile.root.time).reshape((matrix_height, matrix_width))
            count_matrix = np.array(infile.root.counts).reshape((matrix_height, matrix_width))

    except Exception as e:
        print "There has been an error parsing the input file. Please make sure the input data is valid", e
        sys.exit()

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
    # TODO: Do a check for one pixel, the length of timestamps and counts must be equal otherwise error out
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
    try:
        img = Image.fromarray(rgb_matrix, 'RGB')
        img.save(output_image_location)
    except Exception as e:
        print "There has been an error saving the image ", e
        sys.exit()


def validate_input_arguments(output_image_type, input_data_location, output_image_location):
    """
    Function that validates the user input is correct so it can be processed
    :param str output_image_type: Whether the output image is going to be rgb or greyscale
    :param str input_data_location: The file location of the input data
    :param str output_image_location: The file location of the output image. Validate its extension
    :return: Error if there is a problem otherwise returns nothing
    :rtype: None
    """
    filename, file_extension = os.path.splitext(output_image_location)
    # Do error checking making sure run_date is valid date and that input file exists
    if not os.path.isfile(input_data_location):
        print('There has been an error locating the input file. Please make sure this file exists {}'.format(input_data_location))
        sys.exit()

    if output_image_type.lower() != "rgb" and output_image_type.lower() != "greyscale":
        print('Image output type must be equal to greyscale or rgb. Please make sure this argument is correct {}'.format(output_image_type))
        sys.exit()

    if file_extension.lower() != ".jpg" and file_extension.lower() != ".png" and file_extension.lower() != ".jpeg":
        print('Image output file extension must be either jpg, png or jpeg. Please make sure this argument is correct {}'.format(output_image_location))
        sys.exit()


def main():
    """
    Main execution of program that is called when script is ran.
    """
    # parse command line args
    parser = argparse.ArgumentParser(description='This is image generator made by Dean Hutton')
    parser.add_argument('-i', '--input_data', help='Input file location used to generate the images.', required=True)
    parser.add_argument('-ol', '--image_output_location', help='The the file location to save the out image.', required=True)
    parser.add_argument('-ot', '--image_output_type', help="Select out image type. Either 'greyscale' or 'rgb'", required=True)
    args = parser.parse_args()

    output_image_type = args.image_output_type
    input_data_location = args.input_data
    output_image_location = args.image_output_location

    # validate the command line args
    validate_input_arguments(output_image_type, input_data_location, output_image_location)

    # define the matrix height and width
    matrix_width, matrix_height = 256, 256

    # Create a blank 256x256 canvas with all RGB values zeroed out
    zeroed_out_rgb_matrix = np.zeros((matrix_height, matrix_width, 3), dtype=np.uint8)

    # Create data types needed to process. If there was an error exit
    timestamp_matrix, count_matrix = read_and_shape_input_data(input_data_location, matrix_height, matrix_width)

    # Populate the out matrix with the data types. check if greyscale or rgb from input arguments
    if output_image_type.lower() == 'rgb':
        rgb_matrix = populate_rgb_matrix(timestamp_matrix, count_matrix, zeroed_out_rgb_matrix)
    else:
        rgb_matrix = populate_grey_scale_matrix(timestamp_matrix, count_matrix, zeroed_out_rgb_matrix)

    # Save the image to disk
    export_image(rgb_matrix, output_image_location)


if __name__ == "__main__":
    # execute only if run as a script
    main()
