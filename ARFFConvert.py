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

def Instance2ARFF(data, label, configure):
	result = ""
	for i in range(len(data)):
		if configure[i][1] == 'real':
			result = result + str(data[i]) + ','
		elif configure[i][1] == 'integer':
			result = result + str(int(data[i])) + ','
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
	print "Data Preprocessing"
	for i in range(len(totaldata)):
		for j in range(len(totaldata[i])):
			if 'on' in totaldata[i][j]:
				totaldata[i][j] = '1'
			elif 'off' in totaldata[i][j]:
				totaldata[i][j] = '0'
			elif 'stand' in totaldata[i][j]:
				totaldata[i][j] = '0.1'
	for i in range(len(totaldata)):
		for j in range(len(totaldata[i])):
			totaldata[i][j] = float(totaldata[i][j])
	return totaldata

"""
----------------------------------------------
	InputData
	Description:	Get the Input Data
	Hints:	
----------------------------------------------
"""

def InputData(filename):
	FILE = open(filename,'rU')
	rawdata = FILE.read()
	decoded = json.loads(rawdata)
	FILE.close()
	print decoded["totaldata_filename"]
	print decoded["totalclustering_filename"]
	print decoded["configure_filename"]
	print decoded["ARFF_output_filename"]
	#read data
	totaldata = read_dataset(decoded["totaldata_filename"],"\t")
	#read label
	FILE_label = open(decoded["totalclustering_filename"],'rU')
	totallabel = FILE_label.read()
	totallabel = totallabel.split('\n')
	if len(totallabel[totallabel.__len__()-1]) == 0:
		totallabel = totallabel[:-1]
	FILE_label.close()
	#read configure in each parameter
	FILE_configure = open(decoded["configure_filename"],'rU')
	configure = FILE_configure.read()
	configure = configure.split('\n')
	if len(configure[configure.__len__()-1]) == 0:
		configure = configure[:-1]
	for i in range(configure.__len__()):
		configure[i] = configure[i].split('\t')
	FILE_configure.close()
	return 0, decoded["ARFF_output_filename"], totaldata, totallabel, configure

"""
----------------------------------------------
	ARFFHeaderPrint
	Description:	Print the header of ARFF
	Hints:	
---------------------------------------------
"""

def ARFFHeaderPrint(ARFF_Output, configure):
	print configure
	ARFF_Output.write('@RELATION\tinitial_model\n')
	for i in range(len(configure)):
		#print i
		ARFF_Output.write('@ATTRIBUTE\t'+configure[i][0]+'\t'+configure[i][1]+'\n')
	ARFF_Output.write('@ATTRIBUTE\tclass\tinteger\n')
	ARFF_Output.write('@DATA\n')
	return 0
	
totaldata = []
totallabel = []

status, ARFF_output_filename, totaldata, totallabel, configure = InputData(sys.argv[1])
totaldata = DataPreprocessing(totaldata)
print "ARFF_output_filename = ", ARFF_output_filename
ARFF_Output = open(ARFF_output_filename,'w')
ARFFHeaderPrint(ARFF_Output, configure)
for i in range(len(totaldata)):
	ARFF_Output.write(Instance2ARFF(totaldata[i], totallabel[i], configure))
	ARFF_Output.write('\n')
	pass
ARFF_Output.close()
print "Finally..."

	

