import os, sys
import numpy as np
import cv2 as cv 
import csv
# import multiprocessing as mp
from multiprocessing import Process
from collections import OrderedDict
import subprocess
import glob

def perform_train(data_path, cfg_path, pretrained_weight):
	# command_string = "./../darknet detector train ../data/gun.data ../cfg/yolov3_gun.cfg ../darknet53.conv.74 -gpus 1,2,3 -dont_show"
	#print("Inside perform_train")
	command_string = "./darknet detector train "+data_path+" "+cfg_path+" "+pretrained_weight+" -gpus 1,2,3 -dont_show"
	#print(command_string)
	#os.popen(command_string).read()
	#subprocess.call([command_string])
	os.system(command_string)


def perform_inference(data_path, cfg_path, weight_file):
	command_string = "./darknet detector map "+data_path+" "+cfg_path+" "+weight_file+" -gpus 0 -dont_show >> "+weight_file.split(".")[0]+".log"
	#os.popen(command_string).read()
	os.system(command_string)


if __name__ == "__main__": 
	#initialize dictionary for stopping condition with configuration parameters
	f = open('weight_perf_dump/plot_multi_obj.conf','rb')
	line = f.readline()
	param_dict = OrderedDict()
	while(len(line)):
		# print(len(line))
		# print(line)
		line = line.split('\n')[0]
		# print(line)
		param_dict[line.split(' = ')[0]] = (line.split(' = ')[1])
		print(param_dict[line.split(' = ')[0]])
		line = f.readline()
	#f.close()

	params_batch = np.float32( param_dict["BATCH_SIZE"] )
	params_sub_batch = np.float32( param_dict["SUB_BATCH_SIZE"] )
	params_min_epoch = np.float32( param_dict["MIN_EPOCH"] )
	params_max_epoch = np.float32( param_dict["MAX_EPOCH"] )
	params_min_delta = np.float32( param_dict["MIN_DELTA"] )
	params_patience = np.float32( param_dict["PATIENCE"] )
	params_gpu_indx = np.float32( param_dict["GPU_NUM"] )
	params_data_file = str( param_dict["DATA_FILE"] )
	params_cfg_file = str( param_dict["CFG_FILE"] )
	params_names_file = str( param_dict["NAMES_FILE"] )
	params_backup_path = str( param_dict["BACKUP"] )
	params_pretained_weight = str( param_dict["PRETRAINED"] )
	# NEW conditions for new params
	all_map = np.array([])
	# baseline_map = -1
	best_map_iter = -1
	best_map = -1
	epoch_count_baseline = 0
	stop_flag = 0
	#Run train
	first_run = 1
	count_backup_files = 0
	# perform_train( params_data_file, params_cfg_file, params_pretained_weight )
	p = Process(target = perform_train, args = (params_data_file, params_cfg_file, params_pretained_weight,), name = "Perform Train")
	p.start()
	
	weights_logged = []
	#Run test for mAP and F1 score with conditions for stop_flag
	# backup_path = "/home/anerudh/darknet/backup_guns2_test"
	print("starting mAP dump on test set!")
	while(True):
		if(first_run==1):
			count_backup_files = len(os.listdir(params_backup_path)) #int( os.popen("ls "+params_backup_path+"/*.weights -1 | wc -l").read()[:-1] )
			first_run = 0
			csv_filename = 'map_plots_early_stop.csv'
			f0 = open(csv_filename, 'a+')
			writ = csv.writer(f0, delimiter = ',')
			csv_write_list = []
			csv_write_list.append('weight')
			f1 = open(params_names_file)
			line = f1.readline()
			while(len(line)):
				csv_write_list.append( line.split('\n')[0] + '-AP' )
				line = f1.readline()
			csv_write_list.append('F1-score')
			csv_write_list.append('mAP')
			writ.writerow(csv_write_list)
			f0.close()
			print first_run, len(os.listdir(params_backup_path)), count_backup_files
		elif( first_run==0 and count_backup_files < len(os.listdir(params_backup_path)) and len(os.listdir(params_backup_path))>=2 ):
			#int(os.popen("ls "+params_backup_path+" -1 | wc -l").read()[:-1]) and int(os.popen("ls "+params_backup_path+" -1 | wc -l").read()[:-1])>=2 ):
			#new weight file create. Check mAP and stopping condition
			#
			count_backup_files = len(os.listdir(params_backup_path)) #int( os.popen("ls "+params_backup_path+"/*.weights -1 | wc -l").read()[:-1] )
			#weight_file = sorted(os.popen("ls "+params_backup_path).read().split("\n"))[-1]
			files = glob.glob(params_backup_path+'/*')
			files.sort(key=os.path.getmtime)
			weight_file = files[-1]
			
			print( weight_file.split('.')[0].split("_")[-1] )
			if(weight_file.split('.')[0].split("_")[-1] == 'last'):
                        	continue
			
			if(weight_file.split('.')[0].split("_")[-1] in weights_logged):
				continue
			else:
				weights_logged.append(weight_file.split('.')[0].split("_")[-1])
								
			csv_filename = 'map_plots_early_stop.csv'
			f0 = open(csv_filename, 'a+')
			writ = csv.writer(f0, delimiter = ',')
			#
			#csv_write_list = []
			#csv_write_list.append('running inference: start')
			#csv_write_list.append( weight_file.split('.')[0].split("_")[-1] )
			#writ.writerow(csv_write_list)
			
			perform_inference(params_data_file, params_cfg_file, weight_file) #params_backup_path, weight_file)
			
			#csv_write_list = []
                        #csv_write_list.append('running inference: done')
                        #writ.writerow(csv_write_list)
			
			#csv_write_list = []
			#csv_write_list.append('second elif condition reached!')
			#writ.writerow(csv_write_list)
			
			#csv_write_list = []
			#csv_write_list.append(first_run)
			#csv_write_list.append(count_backup_files)
			#csv_write_list.append( int(os.popen("ls "+params_backup_path+" -1 | wc -l").read()[:-1]) )
			#writ.writerow(csv_write_list)
			
			f1 = open(params_names_file)
			line = f1.readline()
			csv_write_list = []
			#if(weight_file.split('.')[0].split("_")[-1] == 'last'):
			#	continue
			csv_write_list.append( weight_file.split('.')[0].split("_")[-1] )
			while(len(line)):
				f2 = open(weight_file.split(".")[-2] +".log")
				line2 = f2.readline()
				while(len(line2)):
					if(line[:-1] in line2 and 'ap' in line2):
						csv_write_list.append( line2.split('\r')[-1].split(' ')[9] )
						#csv_write_list.append( line2.split(" ")[line2.split(" ").index(line[:-1]+",") + 3] )
					line2 = f2.readline()
				line = f1.readline()
			f2 = open(weight_file.split(".")[-2] +".log")
			line2 = f2.readline()
			count = 0
			while(len(line2)):
				if("F1-score" in line2):
					csv_write_list.append( line2.split(" ")[line2.split(" ").index("F1-score") + 2] )
				if("mAP" in line2 and "%" in line2):  
					csv_write_list.append( line2.split(' ')[8] )
					all_map = np.append(all_map, np.float32( line2.split(' ')[8] ))
					count = count +1
				line2 = f2.readline()
			writ.writerow(csv_write_list)
			
			#csv_write_list = []
			#csv_write_list = 'process.pid: ' + str(p.getpid)
			#writ.writerow(csv_write_list)
			
			f0.close()
			
			csv_filename = 'map_plots_early_stop.csv'
                        f0 = open(csv_filename, 'a+')
                        writ = csv.writer(f0, delimiter = ',')
                        
                        csv_write_list = []
                        #csv_write_list.append('running inference: start')
                        #csv_write_list.append( weight_file.split('.')[0].split("_")[-1] )
                        #writ.writerow(csv_write_list)
			
			#if(len(os.listdir(params_backup_path))>=3):
			#	stop_flag = 1
			#	csv_write_list.append('Stop flag:')
			#	csv_write_list.append(stop_flag)
			#	csv_write_list.append('Short cut stop!')
			#	writ.writerow(csv_write_list)
			#	f0.close()
			#	break
						
			epoch = int( weight_file.split(".")[0].split("_")[-1] )
			if(len(all_map)>0):
				if(all_map[-1]>best_map):
					best_map = all_map[-1]
					best_map_iter = epoch
			if(len(all_map)>=2):
				if( (all_map[-1]-all_map[-2])/(all_map[-2]) > params_min_delta ):
					# baseline_map = multi_map[-1]
					epoch_count_baseline = 0
				else:
					epoch_count_baseline = epoch_count_baseline + 1
					if(epoch_count_baseline>= params_patience and epoch > params_min_epoch):
						stop_flag = 1
						csv_write_list.append('Stop flag:')
						csv_write_list.append(stop_flag)
						csv_write_list.append('Patience exhausted!')
						writ.writerow(csv_write_list)
						f0.close()
						break
			if(epoch > params_max_epoch):
				stop_flag = 1
				csv_write_list.append('Stop flag:')
				csv_write_list.append(stop_flag)
				csv_write_list.append('Max Epochs reached')
				writ.writerow(csv_write_list)
				f0.close()
				break
			
			f0.close()
			print(int(os.popen("ls "+params_backup_path+" -1 | wc -l").read()[:-1]))
			print(count_backup_files)
			print('inference done')
			
		#f0 = open(csv_filename, 'a+')
		#writ = csv.writer(f0, delimiter = ',')
		#csv_write_list = []
		#csv_write_list.append(first_run)
		#csv_write_list.append(count_backup_files)
		#csv_write_list.append( int(os.popen("ls "+params_backup_path+" -1 | wc -l").read()[:-1]) )
		#writ.writerow(csv_write_list)
		#f0.close()
		#print(int(os.popen("ls "+params_backup_path+" -1 | wc -l").read()[:-1]))
		#print(count_backup_files)

			
	if (stop_flag):
		#p.join()
		#p.kill()
		#p.shutdown()
                cmd = ["""sudo nvidia-smi |grep ./darknet"""]
                p = subprocess.Popen(cmd, shell =True, stdout=subprocess.PIPE)
                e = p.stdout.read().splitlines()
                oc = []
                for i in e:
                        oc.append(i.split()[2])
                for ID in oc:
                        st="sudo kill -9 "+ID
                        os.system(st)
		#csv_filename = 'map_plots_early_stop.csv'
		#f0 = open(csv_filename, 'a+')
                #writ = csv.writer(f0, delimiter = ',')
                #csv_write_list = []
		#if p.is_alive():
		#	csv_write_list.append("Process is alive , kill it ! ")
		#	writ.writerow(csv_write_list)
		#	#writ.writerow(p)
		#	p.terminate()
		#	csv_write_list =[]
		#	csv_write_list.append("KILLED IT ")
		#	writ.writerow(csv_write_list)
		#	csv_write_list = []
                #csv_write_list.append('Stop condition met!!')
                #writ.writerow(csv_write_list)
		#os.system('sudo kill '+str(p.getpid))
		#print('stop condition met')
		#f0.close()
	
	csv_filename = 'map_plots_early_stop.csv'
        f0 = open(csv_filename, 'a+')
        writ = csv.writer(f0, delimiter = ',')
        csv_write_list = []
        csv_write_list.append('best mAP:')
	csv_write_list.append(str(best_map))
	writ.writerow(csv_write_list)
	csv_write_list = []
	csv_write_list.append('best mAP iter:')
	csv_write_list.append(str(best_map_iter))
	writ.writerow(csv_write_list)
        csv_write_list = []
	csv_write_list.append('best mAP epoch:')
	csv_write_list.append(str( (best_map_iter*params_sub_batch)/params_batch ))
	writ.writerow(csv_write_list)
        #os.system('sudo kill '+str(p.getpid))
        print('stop condition met')
	f0.close()
	
	print("best map: " + str(best_map) )
	print("best map iter = "+ str(best_map_iter) )
	print("best map epoch = "+ str(best_map_iter*params_sub_batch/params_batch) )

	if False: #stop_flag:
		cmd = ["""sudo nvidia-smi |grep ./darknet"""]		
		p = subprocess.Popen(cmd, shell =True, stdout=subprocess.PIPE)
		e = p.stdout.read().splitlines()
		oc = []
		for i in e:
			oc.append(i.split()[2])
		for ID in oc:
			st="sudo kill -9 "+ID
			os.system(st)
	
	#print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@22 exiting@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
	sys.exit(0)




