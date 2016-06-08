# -*- coding: utf-8 -*-

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

import traceback

from tools import read_dataset, Convert2FloatArray

import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.classifiers import Classifier
import weka.plot.classifiers as plot_cls
import weka.plot.graph as plot_graph
import weka.core.types as types

from sklearn import tree, svm, mixture
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.mixture import DPGMM, GMM, VBGMM
import numpy as np

def ModelPossibilityDistribution(clf, instance):
	# this part is designed for scikt-learn
	print "type(instance[0])" , type(instance[0])
	Distribution = clf.predict_proba(instance)
	print Distribution[0]
	return list(Distribution[0])
"""
def ModelPossibilityDistribution(clf, inst):
	#	clf is classifier
	#	inst is arff_instance
	dist = clf.distribution_for_instance(inst)
	return list(dist)
"""
def find_max(inst):
	max_inst = int(inst[0])
	for item in inst:
		if max_inst < int(item):
			max_inst = int(item)
	return max_inst

def ConvertInstance2ARFF(Instance, Clustering):

	FILE = open('BL313_ARFF_header_extracted','rU')
	BL313_ARFF_Header = FILE.read()
	FILE.close()

	Input_Path = "../MARCS_AR_temporary"
	Index = -1
	FILE = open(Input_Path,'w')
	FILE.write(BL313_ARFF_Header)
	FILE.write('\n@ATTRIBUTE class {')
	for i in range((find_max(Clustering))+1):
		if i == 0:
			FILE.write(str(i))
		else:
			FILE.write(','+str(i))
	FILE.write('}\n@DATA')
	for i in range(len(Instance)):
		FILE.write('\n')
		for j in range(len(Instance[i])):
			FILE.write(str(Instance[i][j])+',')
		FILE.write(str(Clustering[i]))
	FILE.write('')
	FILE.close()

	loader = Loader(classname="weka.core.converters.ArffLoader")
	data = loader.load_file(Input_Path)
	data.class_is_last()
	"""
	Input_File = FileReader(Input_Path)
	Training_Data = Instances(Input_File)
	if Index == -1: #
		Training_Data.setClassIndex(Training_Data.numAttributes() - 1)
	else:
		Training_Data.setClassIndex(Index)
	"""
	return data
"""
def Build_DBN_Model(Training_Data):
	DBN_Model = DBN()
	DBN_Model.buildClassifier(Training_Data)
	return DBN_Model

def BuildClassifier(Instance, Clustering, Clustering_Metric):
	# this part is degined for weka
	# Bayes Network is implemented.
	Input_Path ,training_data_arff = Load_Training_Data_ARFF(Instance, Clustering)
	DBN_Classifier = Build_DBN_Model(training_data_arff)
	print "Build Classifier...done..."
	return DBN_Classifier
"""
def BuildClassifier(Instance, Clustering, Clustering_Metric):

	#	the hidden part is designed for scikt-learn
	#clf = GaussianNB()
	#clf = tree.DecisionTreeClassifier()
	#clf = MultinomialNB()
	#clf = tree.ExtraTreeClassifier()
	#clf = svm.SVC(probability=True)
	#clf = DPGMM(n_components = 13)
	#clf = svm.LinearSVC(probability=True)
	#clf = svm.NuSVC(probability=True)
	#clf = KNeighborsClassifier(n_neighbors = 10, weights= "distance")
	#clf = clf.fit(Clustering_Metric, Clustering_Metric_Label)
	#clf = clf.fit(Instance, Clustering)

	Clustering_Metric = np.array(Clustering_Metric)
	Clustering = np.array(Clustering)
	Instance = np.array(Instance)
	Clustering_Metric_Label = []
	for i in range(Clustering_Metric.__len__()):
		Clustering_Metric_Label.append(i)
	Clustering_Metric_Label = np.array(Clustering_Metric_Label)

	#loader = Loader( classname = "weka.core.converters.ArffLoader" )
	#data = ConvertInstance2ARFF(Instance, Clustering)
	#data = ConvertInstance2ARFF(Clustering_Metric, Clustering_Metric_Label)
	#nb = Classifier( classname = "weka.classifiers.bayes.net.EditableBayesNet" )
	#nb.build_classifier(data)
	#return nb

	clf = GaussianNB()
	clf = clf.fit(Clustering_Metric, Clustering_Metric_Label)
	clf = clf.fit(Instance, Clustering)	
	return clf

"""
----------------------------------------------
	isFamilarPattern
	Description:	Check 
	Input:	
	Output:	-1--> no familar pattern, positive integer --> some familar pattern
	Hints:	
----------------------------------------------
"""

FamilarThreshold = 0.9

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
	try:
		decoded = json.loads(rawdata)
	except:
		decoded = {}
	FILE.close()
	return decoded

def print_json_to_file(filename, dict_data):
	FILE = open(filename,'w')
	FILE.write(dict_data)
	FILE.close()
	return 0

"""
----------------------------------------------
	ActivityRecognition
	Description:	Activity Recognition Part. 
	Hints:	In this part, we will read the instance and use the fliter to get the possibility for instance to models.
			If it's old similar label, output it or try to label it
----------------------------------------------
"""

def ActivityRecognition(AR_filename, WL_filename, Semantic_filename, Instance, Clustering, Clustering_Metric):
	pass
	#read the file from AR_filename
	AR_instance = read_dataset(AR_filename,'\t')
	AR_instance = Convert2FloatArray(AR_instance)
	AR_instance_ARFF = ConvertInstance2ARFF(AR_instance, Clustering)
	#read the semantic meaning from extrenal file
	Semantic_Meaning = read_json(Semantic_filename)

	#build classifier for the next step's processing
	clf = BuildClassifier(Instance, Clustering, Clustering_Metric)
	print "type of Semantic_Meaning = ", type(Semantic_Meaning)
	is_unfamilar_pattern = -1
	new_semantic_meaning = False
	#for index, inst in enumerate(AR_instance_ARFF):
	for index, inst in enumerate(AR_instance):
		Distribution = ModelPossibilityDistribution(clf, inst)
		is_familar_pattern = isFamilarPattern(Distribution, Semantic_Meaning)
		print "is_familar_pattern = ", is_familar_pattern
		if is_familar_pattern < 0:
			print "Add a new instance into WaitingList..."
			PrintInstanceWL(AR_instance[index],WL_filename)
		else:
			if Semantic_Meaning.has_key((is_familar_pattern)) == True:
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

def Initialization(filename):
	
	FILE = open(filename,'rU')
	rawdata = FILE.read()
	FILE.close()
	decoded = json.loads(rawdata)
	print "Initial_Instance_filename = ", decoded['Initial_Instance_filename']
	# initial models' instance
	print "Initial_Clustering_filename = ", decoded['Initial_Clustering_filename']
	print "metric_filename = ", decoded['metric_filename']
	# initial models's clustering result

	#read the instance from initial model

	Instance = read_dataset(decoded['Initial_Instance_filename'],'\t')
	Instance = Convert2FloatArray(Instance)

	#read the clustering result from initial instances
	FILE = open(decoded['Initial_Clustering_filename'],'rU')
	Clustering = FILE.read()
	Clustering = Clustering.split('\n')
	while len(Clustering[Clustering.__len__()-1]) == 0:
		Clustering = Clustering[:-1]	
	FILE.close()

	#read the clustering metrics for instances from external file
	
	Clustering_Metric = read_dataset(decoded['metric_filename'],'\t')
	Clustering_Metric = Convert2FloatArray(Clustering_Metric)

	return decoded["log_filename"], decoded["WL_filename"], decoded["Semantic_filename"], Instance , Clustering, Clustering_Metric

"""
----------------------------------------------
	AddModelInstance
	Description:	
	Hints:	
----------------------------------------------
"""

def AddModelInstance(instance_filename, clustering_filename, metric_filename, Instance, Clustering, Clustering_Metric):
	
	AdditionInstance = read_dataset(instance_filename,'\t')

	FILE = open(clustering_filename,'rU')
	AdditionClustering = FILE.read()
	AdditionClustering = AdditionClustering.split('\n')
	while len(AdditionClustering[AdditionClustering.__len__()-1]) == 0:
		AdditionClustering = AdditionClustering[:-1]
	FILE.close()

	Instance = Instance + AdditionInstance
	if min(AdditionClustering) == 0:
		#  if the AdditionClustering starts from 0, it means that we need to relabel AdditionClustering (add the bench of Clustering)
		bench = max(Clustering)+1
		for i in range(AdditionClustering.__len__()):
			AdditionClustering[i] += bench

	Clustering = Clustering + AdditionClustering

	FILE = open(metric_filename,'rU')
	AdditionMetric = FILE.read()
	AdditionMetric = AdditionMetric.split('\n')
	for i in range(AdditionMetric.__len__()):
		AdditionMetric[i] = AdditionMetric[i].split('\t')
		for j in range(len(AdditionMetric[i])):
			AdditionMetric[i][j] = float(AdditionMetric[i][j])
	FILE.close()
	Clustering_Metric = Clustering_Metric + AdditionMetric

	return Instance, Clustering, Clustering_Metric
	
def main():

	log_filename, WL_filename, Semantic_filename, Instance, Clustering, Clustering_Metric = Initialization(sys.argv[1])
	print 'log_filename = ',log_filename
	#log file: print the Activity Recognition Component's Running Log for further processing
	print 'WaitingList_filename = ', WL_filename
	#Waiting List: instance which will be deleted 
	print 'Semantic_filename = ', Semantic_filename
	#Semantic file: save semantic meaning in json format
	
	while True:
		command = raw_input('\nADD:ADD [json file]\nAR:AR [filename]\nplease enter the command:')
		print 'command: '+command
		command = command.split(' ')
		if command[0] == 'ADD' or command[0] == 'Add':
			print "MARCS Update Recognition Model...loading..."
			FILE = open(command[1],'rU')
			rawdata = FILE.read()
			decoded = json.loads(rawdata)
			FILE.close()
			#update the model which is generated by Adaptation Component
			#print "Instance's filename = ", command[1]
			print "Instance's filename = ", decoded["instance_filename"]
			#print "Instance clustering result's filename = ", command[2]
			print "Instance clustering result's filename = ", decoded["clustering_filename"]
			print "Clustering Metric's filename = ", decoded["metric_filename"]
			Instance, Clustering, Clustering_Metric = AddModelInstance(decoded["instance_filename"], decoded["clustering_filename"], decoded["metric_filename"], Instance, Clustering, Clustering_Metric)
			print "MARCS Update Recognition Model...finished."

		if command[0] == 'AR' or command[0] == 'ar':
			print "MARCS Activity Recognition...loading..."
			ActivityRecognition(command[1], WL_filename, Semantic_filename, Instance, Clustering, Clustering_Metric)
			# Input File: like BL313's dataset
			print "MARCS Activity Recognition...finished."
			pass
		pass
	return 0

if __name__=="__main__":
	try:
		jvm.start()
		main()
	except Exception, e:
		print(traceback.format_exc())
	finally:
		jvm.stop()
