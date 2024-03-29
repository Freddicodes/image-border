import argparse
import os

import cv2 as cv
import numpy as np


def get_all_pictures(path: str) -> list:
    jpg_files = []
    for filename in os.listdir(path):
        if filename.endswith('.jpg'):
            jpg_files.append(os.path.join(path, filename))
    return jpg_files


def transform(factor: float, name: str) -> np.ndarray:
    """
    Transform a plain image to an image with white border.
    :param factor: The factor by which the longer of the two sides is scaled.
    :param name: The name of the image that is being transformed.
    :return: The new image with white border.
    """
    # calculating which side to increase and by how much
    image = cv.imread(name)
    h, w = image.shape[:2]
    if w >= h:
        length_result = int(np.round(factor * w))
    else:
        length_result = int(np.round(factor * h))

    # calculating the offset where the original image is placed
    offset_x = (length_result - w) // 2
    offset_y = (length_result - h) // 2

    # creating the resulting image and adding the original image at the offset
    result = np.full((length_result, length_result, 3), fill_value=255, dtype="uint8")
    result[offset_y - 1: offset_y + h - 1, offset_x - 1: offset_x + w - 1] = image

    return result


def setup() -> tuple:
    """
    Set up the argument parser and return the arguments.
    :rtype: tuple
    """
    parser = argparse.ArgumentParser(description="Take an image as input and add a white border to it.")
    parser.add_argument("-f", "--factor", type=float, default=1.1,
                        help="The parameter specifies how much the new image size is scaled up.")
    parser.add_argument("-n", "--name", type=str, default=None,
                        help="The filename of the image that should be converted.")
    parser.add_argument("-a", "--all", type=str, default=None,
                        help="Takes a path to a folder and ads a border to every image in that folder.")
    args = parser.parse_args()

    return args.factor, args.name, args.all


def save_image(image: np.ndarray, path: str) -> None:
    """
    Saves an image with a new name to the same folder as the where it came from.
    :rtype: None
    :param image: The image being saved.
    :param path: The path and name of the image being saved.
    """
    path, name = os.path.split(path)
    name = "border_" + name
    path: str = os.path.join(path, name)
    if not cv.imwrite(filename=path, img=image):
        raise Exception("Could not save the file")


if __name__ == '__main__':
    files = []
    scale_factor, file_name, filepath = setup()

    if file_name is None and filepath is None:
        print("Please use -n (--name) to specify a filename or use -a (--all) to convert all images in a given folder.")

    if file_name is not None:
        files.append(file_name)
    elif file_name is None and filepath is not None:
        files = get_all_pictures(filepath)
    for file_name in files:
        print("Adding border to image: " + file_name)
        global_image = transform(scale_factor, file_name)
        save_image(global_image, file_name)
