# encoding: utf-8

#----------------------------------------------
#	本程序專爲跑碩論數據所準備
#	無法接入Activity Discovery Engine中
#	如果需要接入，需要修改MARCS_Recognition_v2016.py文件
#----------------------------------------------

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

#----------------------------------------------
#	Separate_Instance
#	Description: Separate Instance into micro instance from clustering results
#----------------------------------------------

def Separate_Instance(instance, clustering):
	Micro_Instance = []
	N = find_max(clustering)
	for i in range(N+1):
		Micro = []
		for j in range(clustering.__len__()):
			if clustering[j] == i:
				Micro.append(instance[j])
		Micro_Instance.append(Micro)
	len_micro_dataset = []
	for i in range(Micro_Instance.__len__()):
		len_micro_dataset.append(len(Micro_Instance[i]))
	print "len of micro_dataset = ", len_micro_dataset
	return Micro_Instance

def ND_Build(Micro_Instance):
	ND_clf = []
	for i in range(Micro_Instance.__len__()):
		print "build ND # ",i
		Micro_Instance[i] = np.array(Micro_Instance[i])
		clf = svm.OneClassSVM()
		clf = clf.fit(Micro_Instance[i])
		ND_clf.append(clf)
	return ND_clf

#----------------------------------------------
#	Instance: all data instance
#	Clustering: 
#	TargetInstance: data instance without target label context
#	TargetClustering: clustering results related to TargetInstance
#----------------------------------------------

def ND(ND_clf, instance):
	Distribution = []
	instance = np.array(instance)
	for i in range(ND_clf.__len__()):
		prob = ND_clf[i].predict(instance)[0]
		Distribution.append(prob)
	for i in range(Distribution.__len__()):
		if Distribution[i] > 0:
			return False
	return True


def main():
	
	decoded = read_json(sys.argv[1])
	print decoded

	print "\"",decoded["dataset_filename"],"\""
	Instance = read_dataset(decoded["dataset_filename"],"\t")
	#print Instance
	print len(Instance)
	Instance = Convert2FloatArray(Instance,2)
	Clustering = read_clustering(decoded["clustering_filename"])
	Label = read_label(decoded["label_filename"])

	TargetInstance = read_dataset(decoded["target_dataset_filename"],"\t")
	TargetInstance = Convert2FloatArray(TargetInstance,2)
	TargetClustering = read_clustering(decoded["target_clustering_filename"])
	target_label = decoded["target_label"]

	Micro_TargetInstance = Separate_Instance(TargetInstance, TargetClustering)
	ND_clf = ND_Build(Micro_TargetInstance)

	Recognition_Log = [['context_status','novelty_detection']]
	for i in range(Clustering.__len__()):
		print "instance # = ",i
		if Label[i] in target_label:
			# is target
			status = "novelty"
		else:
			# isn't target
			status = "existing"
		if ND(ND_clf, Instance[i])==True:
			result = "novelty"
		else:
			result = "existing"	
		Recognition_Log.append([status,result])

	TP = 0
	FP = 0
	TN = 0
	FN = 0
	print "end of main...",len(Recognition_Log), " logs..."
	FILE = open(decoded["log_filename"],"w")
	for i in range(Recognition_Log.__len__()):
		FILE.write(Recognition_Log[i][0])
		FILE.write('\t')
		FILE.write(Recognition_Log[i][1])
		FILE.write('\n')
		if Recognition_Log[i][0] == 'novelty' and Recognition_Log[i][1] == 'novelty':
			TP += 1
		if Recognition_Log[i][0] == 'novelty' and Recognition_Log[i][1] == 'existing':
			FN += 1
		if Recognition_Log[i][0] == 'existing' and Recognition_Log[i][1] == 'novelty':
			FP += 1
		if Recognition_Log[i][0] == 'existing' and Recognition_Log[i][1] == 'existing':
			TN += 1

	print [TP,FP,TN,FN]

	FILE.write('TP = '+str(TP)+'\n')
	FILE.write('FP = '+str(FP)+'\n')
	FILE.write('TN = '+str(TN)+'\n')
	FILE.write('FN = '+str(FN)+'\n')

	FILE.close()

if __name__=="__main__":
	main()