import os
import sys
import json
from tools import *

def Initialization(filename):
	FILE = open(filename,'rU')
	rawdata = FILE.read()
	decoded = jumps.loads(rawdata)
	print decoded["WaitingList_filename"]
	print decoded["solid_instance_filename"]
	print decoded["solid_clustering_filename"]
	FILE.close()
	return decoded["WaitingList_filename"], decoded["solid_instance_filename"], decoded["solid_clustering_filename"]

try:
	WL_filename, solid_instance_filename, solid_clustering_filename = Initialization(sys.argv[1])
except:
	exit()

