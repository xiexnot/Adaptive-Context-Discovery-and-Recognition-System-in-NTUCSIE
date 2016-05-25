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
from tools import read_dataset
import traceback
import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.classifiers import Classifier
import weka.plot.classifiers as plot_cls
import weka.plot.graph as plot_graph
import weka.core.types as types



def ModelPossibilityDistribution(instance):
	
	return 0

"""
----------------------------------------------
	isFamilarPattern
	Description:	Check 
	Input:	
	Output:	-1--> no familar pattern, positive integer --> some familar pattern
	Hints:	
----------------------------------------------
"""

FamilarThreshold = 0.95

def isFamilarPattern(Distribution, Semantic_Meaning):
	#not finished yet.
	target = []
	target_semantic = []
	for i in range(len(Distribution)):
		if Distribution[i] > FamilarThreshold:
			target.append(i)
	print "Distribution = ", Distribution
	if len(target) == 0:
		return -1
	if len(target) == 1:
		return target[0]
	if len(target) > 1:
		for i in range(len(target)):
			if Semantic_Meaning.has_key(str(target[i])) == True:
				target_semantic.append(Semantic_Meaning[str(target[i])])
		if len(target_semantic) > 1:
			for item in target_semantic:
				if item != target_semantic[0]:
					return -1
		return target[0]

def PrintInstanceWL(instance, WL_filename):
	FILE = open(WL_filename,'a')
	for i in range(len(instance)):
		if (i != 0):
			FILE.write('\t')
		FILE.write(str(instance[i]))
	FILE.write('\n')
	FILE.close()
	return 0

def read_json(filename):
	FILE = open(filename,'rU')
	rawdata = FILE.read()
	decoded = json.dumps(rawdata)
	FILE.close()
	return decoded

def print_json_to_file(filename, dict_data):
	FILE = open(filename,'w')
	FILE.write(dict_data)
	FILE.close()
	return 0
"""
def ConvertInstance2ARFF(AR_instance, ARFF_header_filename, configure):
	#print data to temporary external file
	FILE = open(ARFF_header_filename, 'rU')
	header = FILE.read()
	FILE.close()
	FILE = open('MARCS_AR_temporary_log','w')
	FILE.write(header)
	for i in range(len(AR_instance)):
		for j in range(len(AR_instance[i])):
			if 'on' in AR_instance[i][j]:
				AR_instance[i][j] = '1'
			elif 'off' in AR_instance[i][j]:
				AR_instance[i][j] = '0'
			elif 'stand' in AR_instance[i][j]:
				AR_instance[i][j] = '0.1'
			if configure[j][1] == integer:
			elif
	
	
	FILE.close()
	loader = Loader(classname="weka.core.converters.ArffLoader")
	return 0
"""
"""
----------------------------------------------
	ActivityRecognition
	Description:	Activity Recognition Part. 
	Hints:	In this part, we will read the instance and use the fliter to get the possibility for instance to models.
			If it's old similar label, output it or try to label it
----------------------------------------------
"""

def ActivityRecognition(AR_filename, WL_filename, Semantic_filename, ARFF_header_filename, configure):
	pass
	#read the file from AR_filename
	AR_instance = read_dataset(AR_filename,'\t')
	AR_instance_ARFF = ConvertInstance2ARFF(AR_instance, ARFF_header_filename, configure)
	#read the semantic meaning from extrenal file
	Semantic_Meaning = read_json(Semantic_filename)

	is_unfamilar_pattern = -1
	new_semantic_meaning = False
	for i in range(len(AR_instance)):
		Distribution = ModelPossibilityDistribution(AR_instance[i])
		is_familar_pattern = isFamilarPattern(Distribution, Semantic_Meaning)
		if is_familar_pattern < 0:
			print "Add a new instance into WaitingList..."
			PrintInstanceWL(AR_instance[i],WL_filename)
		else:
			if Semantic_Meaning.has_key(str(is_familar_pattern)) == True:
				#find propable semantic meaning
				print "AR Result: " + Semantic_Meaning[str(is_familar_pattern)]
			else:
				#cannot find proper semantic mearning
				new_semantic_meaning = True
				semantic_label = raw_input('please enter the Semantic Meaning for the context')
				Semantic_Meaning[str(is_familar_pattern)] = semantic_label

	if new_semantic_meaning == True:
		print_json_to_file(Semantic_filename, Semantic_Meaning)

	return 0

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
	FILE.close()
	#print rawdata
	decoded = json.loads(rawdata)
	print decoded['Initial_ARFF_filename']
	print decoded['configure_filename']

	Initial_ARFF_FILE = open(decoded['Initial_ARFF_filename'],'rU')
	Initial_ARFF = Initial_ARFF_FILE.read()
	Initial_ARFF_FILE.close() 

	FILE = open(decoded['configure_filename'],'rU')
	configure = FILE.read()
	configure = configure.split('\n')
	for i in range(configure.__len__()):
		configure[i] = configure[i].split('\t')
	FILE.close()
	
	return decoded['log_filename'], decoded['WL_filename'], decoded['Semantic_filename'], decoded['ARFF_header_filename'], configure

def main():

	Initial_ARFF = []
	log_filename, WL_filename, Semantic_filename, ARFF_header_filename, configure = Initialization(sys.argv[1], Initial_ARFF)
	print 'log_filename = ',log_filename
	print 'WaitingList_filename = ', WL_filename
	print 'Semantic_filename = ', Semantic_filename
	print "ARFF_header_filename = ", ARFF_header_filename
	print "configure = ", configure

	while True:
		command = raw_input('\nADD:ADD [ARFF\'s filename]\nAR:AR [raw data of dataset\' filename]\nplease enter the command:')
		print 'command: '+command
		command = command.split(' ')
		if command[0] == 'ADD' or command[0] == 'Add':
			print "MARCS Update Recognition Model...loading..."
			#update the model which is generated by Adaptation Component
			print "MARCS Update Recognition Model...finished."
			pass

		if command[0] == 'AR' or command[0] == 'ar':
			print "MARCS Activity Recognition...loading..."
			ActivityRecognition(command[1], WL_filename, Semantic_filename, ARFF_header_filename, configure)
			# Input File: like BL313's dataset
			print "MARCS Activity Recognition...finished."
			pass
		pass
	return 0

if __name__=="__main__":
	jvm.start()
	main()
	jvm.stop()