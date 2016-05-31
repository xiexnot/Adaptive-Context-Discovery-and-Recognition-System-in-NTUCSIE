import os
import sys
import json
from tools import *

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

def main(decoded):
	try:
		WL_filename, Additional_instance_filename, Additional_clustering_filename, Additional_metric_filename = InputData(decoded)
	except:
		exit()
	WL_instance = read_dataset(WL_filename,'\t')
		


if __name__=="__main__":
	decoded = Initialization(sys.argv[1])
	main(decoded)

