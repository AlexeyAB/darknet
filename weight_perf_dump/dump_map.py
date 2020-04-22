
# run woth 'python -tt'
import os, sys
from collections import OrderedDict
import pickle
import pandas
import csv
# os.system("cd ~/gun")
# os.system("ls ../")

# print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# string = "ls ~/darknet/"
# os.system(string)

data_file = "/home/anerudh/darknet/gun2/gun.data"
names_file = "/home/anerudh/darknet/gun2/gun.names"
cfg_file = "/home/anerudh/darknet/gun2/yolov3_gun.cfg"

path_to_weights = "/home/anerudh/darknet/backup_guns/"

list_weights = os.popen("ls "+path_to_weights).read() #~/darknet/backup_guns").read()
list_weights = list_weights.split('\n')[:-1]

for weight in list_weights:
	os.system("./../darknet detector map "+data_file+" "+cfg_file+" "+path_to_weights+weight+" >> "+weight.split(".")[-2]+".log")

csv_filename = 'map_plots.csv'
f0 = open(csv_filename, 'w')
writ = csv.writer(f0, delimiter = ',')

# plot = OrderedDict()
for weight in list_weights:
	plot = OrderedDict()
	f1 = open(names_file)
	line = f1.readline()
	objects = OrderedDict()
	csv_write_list = []
	csv_write_list.append( weight.split('.')[0].split("_")[-1] )
	while(len(line)):
		f2 = open(weight.split(".")[-2] +".log")
		line2 = f2.readline()
		while(len(line2)):
			if(line[:-1] in line2):
				objects[line[:-1]] = line2.split(" ")[line2.split(" ").index(line[:-1]+",") + 3]
				csv_write_list.append( line2.split(" ")[line2.split(" ").index(line[:-1]+",") + 3] )
			line2 = f2.readline()
		line = f1.readline()
	plot["objects"] = objects
	f2 = open(weight.split(".")[-2] +".log")
	line2 = f2.readline()
	count = 0
	while(len(line2)):
		if("F1-score" in line2):
			plot["F1-score"] = line2.split(" ")[line2.split(" ").index("F1-score") + 2]
			csv_write_list.append( line2.split(" ")[line2.split(" ").index("F1-score") + 2] )
		if("mAP" in line2 and "%" in line2):  
			if(True): #count):
				# print(count)
				# print(line2)
				plot["mAP"] = line2.split(' ')[8]
				csv_write_list.append( line2.split(' ')[8] )
			count = count +1
		line2 = f2.readline()
	writ.writerow(csv_write_list)
	pickle_out_file = open(weight.split(".")[-2]+".pckl", "wb")
	pickle.dump(plot, pickle_out_file)
	pickle_out_file.close()

f0.close()



