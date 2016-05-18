"""
	Name:	ARFF Convert designed for MARCS_v2015 
	Algorithm: 
	Input:	Configure for Environment Setting, Clustering Results for instances from MARCS_v2015 Initialized Model, Instance
	Output:	ARFF (with head information) 	
	Description:	
	Date:	2016.05.16
"""

import os
import sys
import math
from tools import read_dataset
import json

"""
----------------------------------------------
	Instance2ARFF
	Description:	Convert instances to ARFF format's instances
	Input:	single instance, single instance's clustering result
	Output:	arff format's single instance(in string format)
----------------------------------------------
"""

def Instance2ARFF(data, label):
	result = ""
	for i in range(len(data)):
		result = result + str(data[i]) + ','
	result += label
	return result

"""
----------------------------------------------
	DataPreprocessing
	Description:	Only process the nomimal value to nominal value.
	Hints:	Not normalization here.
----------------------------------------------
"""

def DataPreprocessing(totaldata):
	for i in range(len(totaldata)):
		for j in range(len(totaldata[i])):
			if 'on' in totaldata[i][j]:
				totaldata[i][j] = '1'
			elif 'off' in totaldata[i][j]:
				totaldata[i][j] = '0'
			elif 'stand' in totaldata[i][j]:
				totaldata[i][j] = '0.1'
	return 0

"""
----------------------------------------------
	InputData
	Description:	Get the Input Data
	Hints:	
----------------------------------------------
"""

def InputData(filename, totaldata, totallabel, configure):
	FILE = open(filename,'rU')
	rawdata = FILE.read()
	decoded = json.loads(rawdata)
	FILE.close()
	print decoded["totaldata_filename"]
	print decoded["totallabel_filename"]
	print decoded["configure_filename"]
	print decoded["ARFF_filename"]
	#read data
	totaldata = read_dataset(decoded["totaldata_filename"],"\t")
	#read label
	FILE_label = open(decoded["totallabel_filename"],'rU')
	totallabel = FILE_label.read()
	totallabel = totallabel.split('\n')
	if len(totallabel[totallabel.__len__()]) == 0:
		totallabel = totallabel[:-1]
	FILE_label.close()
	#read configure in each parameter
	FILE_configure = open(decoded["configure_filename"],'rU')
	configure = FILE_configure.read()
	configure = configure.split('\n')
	if len(configure[configure.__len__()]) == 0:
		configure = configure[:-1]
	FILE_configure.close()
	return 0, decoded["ARFF_output_filename"]

"""
----------------------------------------------
	ARFFHeaderPrint
	Description:	Print the header of ARFF
	Hints:	
---------------------------------------------
"""

def ARFFHeaderPrint(ARFF_Output, configure):

	ARFF_Output.write('@RELATION\tinitial\tmodel\n')
	for i in range(len(configure)):
		ARFF_Output.write('@ATTRIBUTE\t'+configure[i]+'\t'+'REAL\n')
	ARFF_Output.write('@ATTRIBUTE\tclass\tinteger\n')
	ARFF_Output.write('@DATA\n')
	
	return 0
	
totaldata = []
totallabel = []
configure = []

try:
	status, ARFF_output_filename = InputData(sys.argv[1], totaldata, totallabel, configure)
	DataPreprocessing(totaldata)
	ARFF_Output = open(ARFF_output_filename,'w')
	ARFFHeaderPrint(ARFF_Output, configure)
	for i in range(len(totaldata)):
		ARFF_Output.write(Instance2ARFF(totaldata[i], label[i]))
		ARFF_Output.write('\n')
		pass
	ARFF_Output.close()
except:
	exit()
	

