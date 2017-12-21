"""
tests.py
Developer: Dean Hutton
Project: Raster Image Generation
Description: Unit tests for generate_images.py
Date: 12/21/17
"""

import os
import generate_images
import numpy as np
from nose.tools import *


def test_read_and_shape_input_data_with_valid_file():
    """
    Test if the output matrices from the the transform are the correct length
    """
    test_file_path = "%s/%s" % (os.getcwd(), "valid_data.inp")
    timestamp_matrix, count_matrix = generate_images.read_and_shape_input_data(
        test_file_path, 256, 256
    )

    assert len(timestamp_matrix) == 256
    assert len(count_matrix) == 256


@raises(SystemExit)
def test_read_and_shape_input_data_with_invalid_file():
    """
    Test that the script fails with invalid data
    """
    print "here"
    test_file_path = "%s/%s" % (os.getcwd(), "invalid_data.inp")
    timestamp_matrix, count_matrix = generate_images.read_and_shape_input_data(
        test_file_path, 256, 256
    )


def test_populate_grey_scale_matrix_with_valid_data():
    """
    Assert that each value of the RGB pixel is equal for grey scale images
    """
    test_file_path = "%s/%s" % (os.getcwd(), "valid_data.inp")
    timestamp_matrix, count_matrix = generate_images.read_and_shape_input_data(
        test_file_path, 256, 256
    )

    zeroed_out_rgb_matrix = np.zeros((256, 256, 3), dtype=np.uint8)
    rgb_matrix = generate_images.populate_grey_scale_matrix(timestamp_matrix, count_matrix, zeroed_out_rgb_matrix)
    for i, row in enumerate(rgb_matrix):
        for j, rgb in enumerate(row):
            assert rgb[0] == rgb[1] == rgb[2]
            assert rgb[0] <= 256
            assert rgb[1] <= 256
            assert rgb[2] <= 256


def test_populate_rgb_matrix_with_valid_data():
    """
    Assert that each value of the RGB is less than 256
    """
    test_file_path = "%s/%s" % (os.getcwd(), "valid_data.inp")
    timestamp_matrix, count_matrix = generate_images.read_and_shape_input_data(
        test_file_path, 256, 256
    )

    zeroed_out_rgb_matrix = np.zeros((256, 256, 3), dtype=np.uint8)
    rgb_matrix = generate_images.populate_rgb_matrix(timestamp_matrix, count_matrix, zeroed_out_rgb_matrix)
    for i, row in enumerate(rgb_matrix):
        for j, rgb in enumerate(row):
            assert rgb[0] <= 256
            assert rgb[1] <= 256
            assert rgb[2] <= 256


def test_export_image_with_valid_data():
    """
    Assert that an image is created with valid data
    """
    test_file_path = "%s/%s" % (os.getcwd(), "test_output.jpg")
    zeroed_out_rgb_matrix = np.zeros((256, 256, 3), dtype=np.uint8)
    generate_images.export_image(zeroed_out_rgb_matrix, test_file_path)
    assert os.path.isfile(test_file_path)

    # clean up the test file
    os.remove(test_file_path)


@raises(SystemExit)
def test_validate_input_arguments_invalid_image_type():
    """
    Assert the system fails when not using a valid image output type
    """
    test_file_path = "%s/%s" % (os.getcwd(), "test_output.jpg")
    generate_images.validate_input_arguments("not real", test_file_path, test_file_path)


