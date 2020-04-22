import matplotlib.pyplot as plt
import numpy as np 
import cv2 as cv
import os,sys
import pickle
from collections import OrderedDict

folder_path = "/home/anerudh/darknet/weight_perf_dump"

#read config file and get parameters
# old params are DIP_THRESH_PERCENT, DIP_EPOCH_LEN, DIP_EPOCH_PERCENT, LOW_FIRST_N_THRESH, LOW_FIRST_N_EPOCHS
# new params are MIN_EPOCH, MAX_EPOCH, MIN_DELTA, PATIENCE, GPU_NUM
f = open('plot.conf','rb')
line = f.readline()
param_dict = OrderedDict()
while(len(line)):
	# print(len(line))
	# print(line)
	line = line.split('\n')[0]
	# print(line)
	param_dict[line.split(' = ')[0]] = (line.split(' = ')[1])
	line = f.readline()
# f.close()


params_batch = np.float32( param_dict["BATCH_SIZE"] )
params_sub_batch = np.float32( param_dict["SUB_BATCH_SIZE"] )
params_min_epoch = np.float32( param_dict["MIN_EPOCH"] )
params_max_epoch = np.float32( param_dict["MAX_EPOCH"] )
params_min_delta = np.float32( param_dict["MIN_DELTA"] )
params_patience = np.float32( param_dict["PATIENCE"] )
params_gpu_indx = np.float32( param_dict["GPU_NUM"] )

# NEW conditions for new params
multi_map = np.array([])
# baseline_map = -1
best_map_iter = -1
best_map = -1
epoch_count_baseline = 0

stop_flag = 0

# print("hereon")


# uses .pckl file to read performance metrics
for file in sorted(os.listdir(folder_path)):
	if file.endswith(".pckl"):
		f = pickle.load(open(file,'rb'))
		multi_map = np.append(multi_map, np.float32(f['mAP']))
		epoch = int( file.split(".")[0].split("_")[-1] )
		if(multi_map[-1]>best_map):
			best_map = multi_map[-1]
			best_map_iter = epoch
		if(len(multi_map)>=2):
			if( (multi_map[-1]-multi_map[-2])/(multi_map[-2]) > params_min_delta ):
				# baseline_map = multi_map[-1]
				epoch_count_baseline = 0
			else:
				epoch_count_baseline = epoch_count_baseline + 1
				if(epoch_count_baseline>= params_patience and epoch > params_min_epoch):
					stop_flag = 1
					break
		if(epoch > params_max_epoch):
			stop_flag = 1
		# baseline_map = multi_map[-1]
		# f.close()


print("best map: " + str(best_map) )
print("best map iter = "+ str(best_map_iter) )
print("best map epoch = "+ str(best_map_iter*params_sub_batch/params_batch) )


# OLD conditions for old params
# multi_map = np.array([])
# epochs_since_peak = 0
# peak_map_val = 0

# stop_flag = 0
# epochs = 0

# for file in sorted(os.listdir(folder_path)):
# 	if file.endswith(".pckl"):
# 		f = (pickle.load(open(file,'rb')))
# 		multi_map = np.append(multi_map, np.float32(f['mAP']))
# 		if(multi_map[-1]>peak_map_val):
# 			peak_map_val = multi_map[-1]
# 			epochs_since_peak = 0
# 		else:
# 			epochs_since_peak = epochs_since_peak + 1
# 		#stop if map dips for a length of epochs thresh
# 		if(epochs_since_peak==params['DIP_EPOCH_LEN']):
# 			stop_flag = 1
# 		#stop if map dips by a percent thresh and within the length of epochs thresh
# 		if((peak_map_val-multi_map[-1])/peak_map_val > params['DIP_EPOCH_PERCENT'] and epochs_since_peak<params['DIP_EPOCH_LEN']):
# 			stop_flag = 1
# 		#stop if dip is below a thresh on map
# 		if((peak_map_val-multi_map[-1])/peak_map_val > params['DIP_THRESH_PERCENT']):
# 			stop_flag = 1
# 		#stop if map is below a thresh map within an epoch thresh
# 		if(multi_map[-1] < params['LOW_FIRST_N_THRESH'] and epochs < params['LOW_FIRST_N_THRESH']):
# 			stop_flag = 1
# 		plt.plot(multi_map)
# 		plt.show(block=False)
# 		plt.pause(1)
# 		plt.close()
# 		epochs = epochs + 1

