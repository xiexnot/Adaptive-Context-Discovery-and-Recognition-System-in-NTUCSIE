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
	result += ('Context#' + label)
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
	Description:	Only process the nomimal value to nominal value.
	Hints:	Not normalization here.
----------------------------------------------
"""

def InputData(totaldata, totallabel, configure):

	return 0

