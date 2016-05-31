# -*- coding: utf-8 -*-

import os
import sys
import json
from tools import *
from collections import Counter

# import other component of MARCS
from BuildClusterMetric import main as BuildClusterMetricMain
from MARCS_v2015 import main as MARCSMain

def Initialization(filename):
	FILE = open(filename,'rU')
	rawdata = FILE.read()
	decoded = jumps.loads(rawdata)
	FILE.close()
	return decoded

def InputData(decoded):
	print decoded["WaitingList_filename"]
	print decoded["Additional_instance_filename"]
	print decoded["Additional_clustering_filename"]
	print decoded['Additional_metric_filename']
	return decoded["WaitingList_filename"], decoded["Additional_instance_filename"], decoded["Additional_clustering_filename"], decoded['Additional_metric_filename']

#	Clustering_Frequency_Count
#	Input:	Clustering_Result
#	Output:	Counter {clustering_item:counting} 

def Clustering_Frequency_Count(clustering):
	count = Counter(clustering)
	count = dict(count)
	return count

def Adaptation(instance, clustering, count):
	print "Adaptation...start..."
	count_list = list(count)
	count_total_number = 0
	for item in count_list:
		count_total_number += count[item]
	clustering_success = []
	clustering_remain = []
	for item in count_list:
		if float(count[item]) / float(count_list) > 0.4:
			pass
			clustering_success.append(item)
		else:
			clustering_remain.append(item)
	print "clustering_success = ", clustering_success
	print "clustering_remain = ", clustering_remain

	for item in range(clustering.__len__()):
		if clustering[item] in clustering_success:
			# item-th's instance is successful for adaptation
			instance_success.append(instance[item])
		else:
			# item-th's instance is remained to be processed
			instance_remain.append(instance[item])

	return instance_success, instance_remain

def print_dataset(filename, dataset, split_symbol, blank_ending_line):
	#if blank_ending_line = true ---> print blank line in the end of file
	FILE = open(filename,'rU')
	for i in range(dataset.__len__()):
		if i != 0:
			FILE.write('\n')
		for j in range(len(dataset[i])):
			if j != 0:
				FILE.write(split_symbol)
			FILE.write(str(dataset[i][j]))
	if blank_ending_line == True:
		FILE.write('\n')
	FILE.close()
	return 0

def main(decoded):
	try:
		WL_filename, Additional_instance_filename, Additional_clustering_filename, Additional_metric_filename = InputData(decoded)
	except:
		exit()
	WL_instance = read_dataset(WL_filename,'\t')
	
	#对WL进行分群
	WL_clustering = MARCSMain({ "dataset_filename":WL_filename, "Pinit":0, "eigenvalue_sum_threshold":0.9 })
	#统计WL的每个分群结果出现的频率
	WL_clustering_counter = Clustering_Frequency_Count(WL_clustering)

	#判断某一个WL_clustering是否可以被归为新的群的数据
	#输入：WL_clustering_counter
	#输出：可以被归为新活动的instance - WL_instance_success (list) 以及剩余的活动 WL_instance_remain

	WL_instance_success, WL_instance_remain = Adaptation(WL_instance, WL_clustering, WL_clustering_counter)

	#更新WL文件为WL_instance_remain
	print_dataset(WL_filename,WL_instance_remain,'\t',True)

if __name__=="__main__":
	decoded = Initialization(sys.argv[1])
	main(decoded)

