# Program that calculates the average precision for each class of a darknet classifier model weight
# As inputs it needs the model condifuration and data file and the weight file.
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

    meta_file_content = open(meta_path, "r").read()
    match = re.search("labels *= *(.*)$", meta_file_content,
                      re.IGNORECASE | re.MULTILINE)
    # If names file found return it as a string list
    if match:
        names_filename = match.group(1)
        if os.path.exists(names_filename):
            names_file = open(names_filename, "r")
            names = names_file.read().strip().split("\n")
            altNames = [x.strip() for x in names]


# Return validation files fetched the configuration file.
def get_validation_files(meta_path):
    # Try to read the names file from the cfg file
    meta_file_content = open(meta_path, "r").read()

    # Search for valid files
    match = re.search("valid *= *(.*)$", meta_file_content,
                      re.IGNORECASE | re.MULTILINE)
    if match:
        valid_filename = match.group(1)
        if os.path.exists(valid_filename):
            valid_file = open(valid_filename, "r")
            valid_files = valid_file.read().strip().split("\n")

    return valid_files


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


# Program that calculates the average precision for each class of a darknet classifier model weight.
# As inputs it needs the model condifuration and data file and the weight file.
def YOLO():
    # If the user does not satisfy the program argument number, show a message error.
    if ((len(sys.argv) < 4) | (len(sys.argv) > 5)):
        print(
            "usage: python3 darknet_classify.py <cfg-file> <data-file> <weights>")
        return

    # Read necessary files for the classifier from command line arguments
    config_path, meta_path, weight_file = sys.argv[1:4]
    valid_files = get_validation_files(meta_path)

    configure(config_path, weight_file, meta_path)

    classes_precision = {}
    for name in altNames:
        classes_precision[name] = [0, 0]  # Correct, Incorrect

    for valid_file in valid_files:
        desired_class_name = valid_file.split("/")[-1].split("_")[1][:-4]
        detected_class_name = clasifyImage(valid_file).split(" - ")[0]

        if (detected_class_name == desired_class_name):
            classes_precision[desired_class_name][0] += 1
        else:
            classes_precision[desired_class_name][1] += 1

    total_precission = 0
    for class_name in classes_precision.keys():
        correct_number = classes_precision[class_name][0]
        incorrect_number = classes_precision[class_name][1]
        total_number = correct_number + incorrect_number

        ap = float(correct_number / total_number)
        total_precission += ap
        print("Precission of " + class_name + ": " + str(ap) + " (C = " +
              str(correct_number) + ", I = " + str(incorrect_number) + ")")

    print("Average precision: " +
          str(float(total_precission / len(classes_precision.keys()))))


if __name__ == "__main__":
    YOLO()
