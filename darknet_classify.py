# Program to classify images. There are two modes:
#  - Single classification: The user passes an input-img at the end of the argument lists
# and the program classify it.
#  - Multiple classification: The program prompt an image path and classify that image.
# It loops until the user types 'exit'
#
# Author: [Ángel Igareta](https://github.com/angeligareta)
from ctypes import *
import darknet
import math
import cv2
import sys
import os
import re


# Raises error text
def raiseInvalidFile(file_type, file_path):
    raise ValueError("Invalid " + file_type + "path: " + file_path)


# Configures the yolo network, 
def configure(config_path, weights_path, meta_path):
    # As we are modifying them from darknet
    global netMain, metaMain, altNames

    if not os.path.exists(config_path):
        raiseInvalidFile("config", os.path.abspath(config_path))
    if not os.path.exists(weights_path):
        raiseInvalidFile("weights", os.path.abspath(weights_path))
    if not os.path.exists(meta_path):
        raiseInvalidFile("meta", os.path.abspath(meta_path))

    # Load YOLO network
    netMain = darknet.load_net_custom(config_path.encode("ascii"),
                                      weights_path.encode("ascii"), 
                                      0, 
                                      1)  # batch size = 1
    # Load data file to YOLO network
    metaMain = darknet.load_meta(meta_path.encode("ascii"))

    # Try to read the names file from the cfg file
    meta_file_content = open(meta_path, "r").read()
    match = re.search("names *= *(.*)$", meta_file_content,
                        re.IGNORECASE | re.MULTILINE)
    # If names file found return it as a string list
    if match:
        names_filename = match.group(1)
        if os.path.exists(names_filename):
            names_file = open(names_filename, "r")
            names = names_file.read().strip().split("\n")
            altNames = [x.strip() for x in names]


# Classify an image in the image path received by argument and
# returns the top detection class and its probability for that image
def clasifyImage(image_path):
    if os.path.isfile(image_path):
        # Read image using video capture as the YOLO Python API use it
        cap = cv2.VideoCapture(image_path)

        # Create a darknet image
        darknet_image = darknet.make_image(darknet.network_width(
            netMain), darknet.network_height(netMain), 3)

        # Read the image, set the correct color and resize it. The resulting image is saved in darknet_image
        ret, frame_read = cap.read()
        frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (darknet.network_width(
            netMain), darknet.network_height(netMain)), interpolation=cv2.INTER_LINEAR)
        darknet.copy_image_from_bytes(darknet_image, frame_resized.tobytes())

        # Classify the image
        detections = darknet.classify(netMain, metaMain, darknet_image)

        # Only return top detection in thhe format 'class_name - probability'
        top_detection = detections[0]
        class_name, probability = top_detection
        return (class_name.decode("utf-8") + " - " + str(probability))
    else:
        return ("File " + image_path + " not found")


# Program to classify images. There are two modes:
#  - Single classification: The user passes an input-img at the end of the argument lists
# and the program classify it.
#  - Multiple classification: The program prompt an image path and classify that image.
# It loops until the user types 'exit'
def YOLO():
    # If the user does not satisfy the program argument number, show a message error.
    if ((len(sys.argv) < 4) | (len(sys.argv) > 5)):
        print(
            "usage: python3 darknet_classify.py <cfg-file> <weights-file> <data-file> [<input-img>]")
        return

    # Read necessary files for the classifier from command line arguments
    config_path, weight_path, meta_path = sys.argv[1:4]
    configure(config_path, weight_path, meta_path)

    if (len(sys.argv) == 5):  # If the user entered an input img, classify it
        image_path = sys.argv[-1]
        detected_text = clasifyImage(image_path)
        print(detected_text)
    else:  # In other case, loop detecting an image per iteration until the user types exit.
        while True:
            image_path = input("Image Path to classify: ")
            if image_path == "exit":
                break
            else:
                detected_text = clasifyImage(image_path)
                print(detected_text)


if __name__ == "__main__":
    YOLO()