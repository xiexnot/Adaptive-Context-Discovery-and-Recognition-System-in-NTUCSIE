# encoding: utf-8

#	源文件是MARCS_Recognition.py
#	写完硕论初稿之后发现增加了多层novelty detection的部分
#	实在不想去改原来的MARCS_Recognition.py（其实是已经改不动了）
#	所以重写了Recognition

import os
import sys
import math
import json

from sklearn import tree, svm, mixture
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.mixture import DPGMM, GMM, VBGMM
import numpy as np

from tools import *

def Initialization(filename):
	
	FILE = open(filename,'rU')
	rawdata = FILE.read()
	FILE.close()
	decoded = json.loads(rawdata)
	print "Initial_Instance_filename = ", decoded['Initial_Instance_filename']
	print "Initial_Clustering_filename = ", decoded['Initial_Clustering_filename']
	#print "metric_filename = ", decoded['metric_filename']
	print "feature filename = ", decoded["feature_filename"]
	#metric 在 master thesis中用不太到

	print "sub context = ",decoded["sub"]

	Sub_Feature  =[]
	Sub_Clustering = []
	Sub_Instance = []
	for i in range(len(decoded["sub"])):
		print "#",i," sub processing..."
		print decoded["sub"][i]
		print decoded["sub"][i]["feature_filename"]
		print decoded["sub"][i]["clustering_filename"]
		print decoded["sub"][i]["instance_filename"]
		Sub_Feature_item = read_feature(decoded["sub"][i]["feature_filename"])
		Sub_Clustering_item = read_clustering(decoded["sub"][i]['clustering_filename'])
		Sub_Instance_item, tmp = read_dataset(decoded["sub"][i]["instance_filename"],'\t')
		Sub_Instance_item = Convert2FloatArray(Sub_Instance_item,2)
		Sub_Feature.append(Sub_Feature_item)
		Sub_Clustering.append(Sub_Clustering_item)
		Sub_Instance.append(Sub_Instance_item)

	print "end of sub information"
	Instance, tmp = read_dataset(decoded['Initial_Instance_filename'],'\t')
	Instance = Convert2FloatArray(Instance,2)
	Feature = read_feature(decoded['feature_filename'])

	#read the clustering result from initial instances
	Clustering = read_clustering(decoded['Initial_Clustering_filename'])

	#Clustering_Metric = read_dataset(decoded['metric_filename'],'\t')
	#Clustering_Metric = Convert2FloatArray(Clustering_Metric)
	#return decoded["log_filename"], decoded["WL_filename"], decoded["Semantic_filename"], Instance , Clustering, Clustering_Metric

	print "Initialization()...Completed..."
	return decoded['log_filename'], decoded['WL_filename'], decoded['Semantic_filename'], Instance, Clustering, Feature, Sub_Instance, Sub_Clustering, Sub_Feature

"""

def ActivityRecognition(AR_filename, WL_filename, Semantic_filename, Instance, Clustering):
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

#----------------------------------------------
#	Novelty Detecting
#	Description: Detect the potential novelty by using ND Classifier
#----------------------------------------------

def all_potential_novelty(Distribution):
	count = 0
	for i in range(Distribution.__len__()):
		if Distribution[i] < -0.5:
			count += 1
	if count == Distribution.__len__():
		return True
	else:
		return False

def Novelty_Detecting(instance, ND_Classifier, Sub_Feature):
	result = False
	print "Novelty Detecting..."
	print Sub_Feature
	print instance

	for i in range(0,ND_Classifier.__len__()):
		sub_instance = []
		print "# of feature = ", len(Sub_Feature[i])
		for j in range(len(Sub_Feature[i])):
			sub_instance.append(instance[Sub_Feature[i][j][0]])
		print sub_instance
		sub_instance = np.array(sub_instance)
		
		Distribution = []
		for j in range(len(ND_Classifier[i])):
			distribution = ND_Classifier[i][j].predict(sub_instance)[0]
			print i,"#",j," = ", distribution
			Distribution.append(distribution)
		print "Distribution for ",i,"-th ND = ", Distribution
		if all_potential_novelty(Distribution) == True:
			return True
	return result

#----------------------------------------------
#	ActivityRecognition
#	Description:	Check whether Novelty Detection occurs.
#					If novelty occurs, add the related instance into WL
#----------------------------------------------

def ActivityRecognition(AR_filename, Feature, WL_filename, Semantic_filename, ND_Classifier, Sub_Feature):

	AR_instance, line = read_dataset(AR_filename,'\t')
	print "AR_instance = ",AR_instance
	AR_instance = Convert2FloatArray(AR_instance,2)
	Semantic_Meaning = read_json(Semantic_filename)

	print "AR_instance = ",AR_instance
	if Novelty_Detecting(AR_instance[0], ND_Classifier, Sub_Feature) == True:
		print "Novelty...Detected!..."
	else:
		print "Existing Context...Detected..."
	return 0

#----------------------------------------------
#	one_class_ND
#	Description:	Build up one class classifier with given instances
#----------------------------------------------

def one_class_ND(index, instance):
	clustering = []
	for i in range(instance.__len__()):
		clustering.append(index)
	print "one_class_ND ", len(instance)," ",len(clustering)
	instance = np.array(instance)
	clustering = np.array(clustering)
	clf = svm.OneClassSVM()
	clf = clf.fit(instance, clustering)
	return clf

#----------------------------------------------
#	ND_Classifier_BUILD
#	Description:	Build up single Sub or Micro Novelty Detection Classifier
#	Hints:	
#	ND_Classifier_Sub[i]: 	one-class Novelty Detection for i-th context
#----------------------------------------------

def ND_Classifier_BUILD(Instance, Clustering):
	pass
	ND_Classifier_Sub = []
	M = find_max(Clustering)
	print "ND Classifier # = ", M
	for i in range(M+1):
		instance = []
		#create instances which are only related to corresponding context
		for x in range(Clustering.__len__()):
			if Clustering[x] == i:
				instance.append(Instance[x])
		clf = one_class_ND(i, instance)
		ND_Classifier_Sub.append(clf)
	return ND_Classifier_Sub

#----------------------------------------------
#	NoveltyDetection_BUILD
#	Description:	Build up All Sub or Micro Novelty Detection Classifier
#	Hints:	
#	Sub_Instance[i]: i-th sub dataset
#	Sub_Clustering[i]: i-th sub clustering result
#	Sub_Instance[i][j]: j-th instance in i-th sub dataset
#----------------------------------------------


def Small_Test(ND_Classifier):
	instance = [1.0,0.0,0.0,0.0,0.0]
	for i in range(len(ND_Classifier[0])):
		print "Small Test #",i
		print ND_Classifier[0][i].predict(instance)

	return 0

def NoveltyDetection_BUILD(Sub_Instance, Sub_Clustering):
	print "NoveltyDetection_BUILD()..."
	ND_Classifier = []
	N = Sub_Instance.__len__()
	for i in range(N):
		print "#",i," Novelty Detection Classifier"
		ND_Classifier_item = ND_Classifier_BUILD(Sub_Instance[i],Sub_Clustering[i])
		ND_Classifier.append(ND_Classifier_item)
	print "NoveltyDetection_BUILD()...Completed..."
	Small_Test(ND_Classifier)
	return ND_Classifier

#----------------------------------------------
#	Halt_For_Test
#	Description:	Halt the program for testing
#----------------------------------------------

def Halt_For_Test():
	while (1):
		pass
	pass

#----------------------------------------------
#	Main
#----------------------------------------------

def main():

	log_filename, WL_filename, Semantic_filename, Instance, Clustering, Feature, Sub_Instance, Sub_Clustering, Sub_Feature = Initialization(sys.argv[1])
	ND_Classifier = NoveltyDetection_BUILD(Sub_Instance, Sub_Clustering)
	
	print "===================================="
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
			#print "Clustering Metric's filename = ", decoded["metric_filename"]
			Instance, Clustering, Clustering_Metric = AddModelInstance(decoded["instance_filename"], decoded["clustering_filename"], decoded["metric_filename"], Instance, Clustering, Clustering_Metric)
			print "MARCS Update Recognition Model...finished."

		if command[0] == 'AR' or command[0] == 'ar':
			print "MARCS Activity Recognition...loading..."
			#ActivityRecognition(command[1], WL_filename, Semantic_filename, Instance, Clustering, Clustering_Metric)
			ActivityRecognition(command[1], Feature, WL_filename, Semantic_filename, ND_Classifier, Sub_Feature)
			print "MARCS Activity Recognition...finished."
			pass
		pass
	return 0


if __name__=="__main__":
	try:
		#jvm.start()
		main()
	except Exception, e:
		#print(traceback.format_exc())
		pass
	finally:
		#jvm.stop()
		pass



