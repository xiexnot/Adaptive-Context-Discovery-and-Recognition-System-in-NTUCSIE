import os
import sys
import json
from tools import *

def Initialization(filename):
	FILE = open(filename,'rU')
	rawdata = FILE.read()
	decoded = jumps.loads(rawdata)
	print decoded["WaitingList_filename"]
	print decoded["Additional_instance_filename"]
	print decoded["Additional_clustering_filename"]
	print decoded['Additional_metric_filename']
	FILE.close()
	return decoded["WaitingList_filename"], decoded["Additional_instance_filename"], decoded["Additional_clustering_filename"], decoded['Additional_metric_filename']

try:
	WL_filename, Additional_instance_filename, Additional_clustering_filename, Additional_metric_filename = Initialization(sys.argv[1])
except:
	exit()



