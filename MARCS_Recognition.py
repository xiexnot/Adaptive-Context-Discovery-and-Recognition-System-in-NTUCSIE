"""
	Name:	MARCS_Online_Recognition for online recognizing 
	Algorithm:	
	Description:	
	Hints:	
	Date:	
"""
import os
import sys
import math
import json
import weka.core.jvm as jvm

"""
----------------------------------------------
	Initialization
	Description:	read the initial model
	Hints:	
----------------------------------------------
"""

def Initialization(filename, Initial_ARFF):
	
	FILE = open(filename,'rU')
	rawdata = FILE.read()
	print rawdata
	decoded = json.loads(rawdata)
	print decoded['Initial_ARFF_filename']
	Initial_ARFF_FILE = open(decoded['Initial_ARFF_filename'],'rU')
	Initial_ARFF = Initial_ARFF_FILE.read()
	Initial_ARFF_FILE.close() 
	FILE.close()
	return decoded['log_filename'], decoded['WL_filename']

Initial_ARFF = []
log_filename, WL_filename = Initialization(sys.argv[1], Initial_ARFF)
print 'log_filename = ',log_filename
print 'WaitingList_filename = ', WL_filename
exit()

while True:
	command = raw_input('\nADD:ADD [ARFF\'s filename]\n AR:AR [raw data of dataset\' filename]\nplease enter the command:')
	print 'command: '+command
	command = command.split(' ')
	if command[0] == 'ADD' or command[0] == 'Add':
		pass
	if command[0] == 'AR' or command[0] == 'ar':
		pass

	pass
