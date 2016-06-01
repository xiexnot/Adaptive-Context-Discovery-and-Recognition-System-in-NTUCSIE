#
#	Build Cluster Metric.py
#

import os
import sys
import math
import json

"""
import weka.core.jvm as jvm
from tools import read_dataset
import traceback
import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.classifiers import Classifier
import weka.plot.classifiers as plot_cls
import weka.plot.graph as plot_graph
import weka.core.types as types
"""

from sklearn import tree, svm, mixture
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
import numpy as np
from tools import read_dataset

from tools import Convert2FloatArray

def initialization(input_json_filename):
	print input_json_filename
	FILE = open(input_json_filename,'rU')
	rawdata = FILE.read()
	decoded = json.loads(rawdata)
	FILE.close()
	return decoded

def main(decoded):

	print decoded["clustering_filename"]
	print decoded["dataset_filename"]
	print decoded["metric_filename"]
	
	instance = read_dataset(decoded["dataset_filename"],'\t')

	FILE = open(decoded["clustering_filename"],'rU')
	clustering = FILE.read()
	clustering = clustering.split('\n')
	if clustering[clustering.__len__()-1]:
		clustering = clustering[:-1]
	FILE.close()

	instance = Convert2FloatArray(instance)

	for i in range(clustering.__len__()):
		clustering[i] = int(clustering[i])

	max_no = max(clustering)

	clustering_head = []
	for cluster_item in range(max_no+1):
		item = []
		for i in range(len(instance[0])):
			item.append(0.0)
		count = 0
		for i in range(clustering.__len__()):
			if clustering[i] == cluster_item:
				count += 1
				for j in range(len(instance[i])):
					item[j] += instance[i][j]
		for i in range(item.__len__()):
			item[i] = round(item[i] / float(count), 2)
		clustering_head.append(item)

	FILE = open(decoded["metric_filename"],'w')
	print clustering_head
	for i in range(clustering_head.__len__()):
		if i!=0:
			FILE.write('\n')
		for j in range(len(clustering_head[i])):
			if j != 0:
				FILE.write('\t')
			FILE.write(str(clustering_head[i][j]))
	FILE.close()

######################################

	clustering_head_label = []
	for i in range(clustering_head.__len__()):
		clustering_head_label.append(i)

	return clustering_head, clustering_head_label

"""
	clf = svm.SVC(probability = True)
	clf = tree.DecisionTreeClassifier()

	clf = tree.ExtraTreeClassifier()
	clf = clf.fit(clustering_head, clustering_head_label)

	FILE = open('BL313_test_instance','rU')
	test = FILE.read()
	test = test.split('\t')
	print test
	for i in range(test.__len__()):
		if 'on' in test[i]:
			test[i] = '1'
		elif 'off' in test[i]:
			test[i] = '0'
		elif 'stand' in test[i]:
			test[i] = '0.1'
		test[i] = float(test[i])
	test = [test]
	FILE.close()

	print clf.predict_proba(test)
"""
	

if __name__ == "__main__":
	decoded = initialization(sys.argv[1])
	main(decoded)
