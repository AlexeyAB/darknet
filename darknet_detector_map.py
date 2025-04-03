# Program that calculates the mean average precission for each one of the weights contained
# in the input parameter <weights-folder>, annotate the precission for that weight and returns
# a ranking with the weights sorted by their precission.
# Author: [Ángel Igareta](https://github.com/angeligareta)
from ctypes import *
import subprocess
import darknet
import math
import cv2
import sys
import os
import re


# Variable to indicate if the wieghts under the top 10 should be removed.
REMOVE = False


# Check if file exists, if not raise value error.
def checkFile(file_type, file_path):
    if not os.path.isfile(file_path):
        raise ValueError("Invalid " + file_type + "path: " + file_path)


# Check if directory exists, if not raise value error.
def checkDir(file_type, file_path):
    if not os.path.isdir(file_path):
        raise ValueError("Invalid " + file_type + "path: " + file_path)


# Show weights ranking
def show_weights_rank(weights_map):
    counter = 1
    for weight_file in sorted(weights_map.items(), key=lambda kv: kv[1], reverse=True):
        print(str(counter) + "º position: " +
              weight_file[0] + " with a probability of " + str(weight_file[1]))
        counter += 1


# This method (if the flag REMOVE is activated) sorts the current weights collection acording to its precission
# and remove the ones under the top-10 ranking
def ask_remove(weights_map, weights_folder_path):
    if REMOVE:
        print("Feasible weights to remove:")
        weights_to_remove = sorted(
            weights_map.items(), key=lambda kv: kv[1], reverse=True)[9:]
        for weight_file in weights_to_remove:
            print(weight_file[0] +
                  " with a probability of " + str(weight_file[1]))

        #option = input("Do you want to remove the following not top-10 weights:\n")
        # if (option == 'yes'):
        for weight_file in weights_to_remove:
            weight_path = weights_folder_path + "/" + weight_file[0]
            del weights_map[weight_file[0]]
            os.remove(weight_path)
        print("Removed!")


# Program that calculates the mean average precission for each one of the weights contained
# in the input parameter <weights-folder>, annotate the precission for that weight and returns
# a ranking with the weights sorted by their precission.
def YOLO():
    # If the user does not satisfy the program argument number, show a message error.
    if (len(sys.argv) != 4):
        print(
            "usage: python3 darknet_detection_map.py <cfg-file> <data-file> <weights-folder>")
        return

    # Read necessary files for the classifier from command line arguments
    config_path, meta_path, weights_folder_path = sys.argv[1:4]
    checkFile('config', config_path)
    checkFile('data', meta_path)
    checkDir('weights', weights_folder_path)

    # Start executing detector map
    counter = 0
    weights_map = {}
    for weight_file in os.listdir(weights_folder_path):
        output = subprocess.check_output(
            ['./darknet', 'detector', 'map',
             meta_path,
             config_path,
             weights_folder_path + "/" + weight_file,
             '-points', '0'])
        mean_average_precission = float(output.decode(
            'utf8').split("\n")[-7].split(" ")[-5][:-1])
        weights_map[weight_file] = mean_average_precission
        print("Precission of " + weight_file +
              " is: " + str(mean_average_precission))

        counter += 1
        if (counter % 10 == 0):
            print("- " + str(counter).upper() + " WEIGHTS RANK -")
            show_weights_rank(weights_map)
            ask_remove(weights_map, weights_folder_path)

    # Print final weights ranking according to its precission.
    print("- FINAL WEIGHTS RANK -")
    show_weights_rank(weights_map)
    ask_remove(weights_map, weights_folder_path)


if __name__ == "__main__":
    YOLO()