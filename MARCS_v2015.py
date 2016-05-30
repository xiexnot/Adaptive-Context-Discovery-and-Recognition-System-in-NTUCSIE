"""
	Name:	MARCS_v2015 for initialized unsupervised modelling 
	Algorithm:	PCA+DAP
	Description:	
	Hints:	This program's initial version was proposed by Andy Zong-Chi Chiang in 2015.
	Date:	2016.05.09
"""

"""
----------------------------------------------
	Input:	Environmental status dataset in the format like BL313
	Output:	1. Clustering Results for all dataset 2. sub-dataset in the same clustering results. 
----------------------------------------------
"""

from tools import *
import os
import sys
from pca import pca_raw_cov as pca
import copy
import json
import copy

"""
----------------------------------------------
	find_max
	Description:
	Hints:	
	Input:
	Output:
----------------------------------------------
"""

def find_max(x):
	max_value = 0
	for i in range(len(x)):
		if int(x[i][0]) > max_value:
			max_value = int(x[i][0])
	return max_value
	
"""
----------------------------------------------
	InputData
	Description: read the dataset from sys.argv[1]
	Input:	N/A
	Output:	N/A
----------------------------------------------
"""
	
def InputData(input_json_filename):
	#global d
	#global eigenvalue_sum_threshold, Pinit
	#global eigenvalue_filename, eigenvector_filename, cluster_filename
	if input_json_filename.__len__() == 0:
		print "python [python's filename] [json's filename]"
		exit()
	FILE = open(input_json_filename,"rU")
	rawdata = FILE.read()
	decoded = json.loads(rawdata)
	print rawdata	
	print decoded['dataset_filename']
	print decoded['eigenvalue_sum_threshold']
	print decoded['Pinit']
	print decoded['eigenvalue_filename']
	print decoded['eigenvector_filename']
	print decoded['cluster_filename']
	
	FILE.close()
	#Pinit = int(decoded['Pinit'])
	#eigenvalue_sum_threshold = float(decoded['eigenvalue_sum_threshold'])
	#eigenvector_filename = copy.deepcopy(decoded['eigenvector_filename'])
	#eigenvalue_filename = copy.deepcopy(decoded['eigenvalue_filename'])
	#cluster_filename = copy.deepcopy(decoded['cluster_filename'])
	return decoded['dataset_filename'], decoded['eigenvalue_sum_threshold'], decoded['Pinit'], decoded['eigenvalue_filename'], decoded['eigenvector_filename'], decoded['cluster_filename']
	
"""
----------------------------------------------
	ConvertDataFormat
	Description: Convert dataset into real number format 
	Steps: 1. convert 'on' 'off' 'stand' into real number(this is specially for BL313) 2. 
	Input: d(dataset)
	Output: 0 for success, 1 for some error
----------------------------------------------
"""
	
def ConvertDataFormat(d):
	#global d
	for i in range(len(d)):
		for j in range(len(d[i])):
			if 'on' in d[i][j]:
				d[i][j] = 1
			elif 'off' in d[i][j]:
				d[i][j] = 0.1
			elif 'stand' in d[i][j]:
				d[i][j] = 0
	print "start to convert to float"
	try:
		d = [[float(j) for j in i] for i in d]
		print 'start to convert to float...done...'
	except:
		for i in range(len(d)):
			for j in range(len(d[i])):
				try:
					d[i][j] = float(d[i][j])
				except:
					print i,"\t",j,"\t",d[i][j]
					return 1
	return d

"""
----------------------------------------------
	DatasetNormalization
	Description:Normalize the input dataset
	Input:	d(dataset)
	Output: 0 for success
----------------------------------------------
"""

def DatasetNormalization(d):
	print "start to zip"
	dt = zip(*d)
	print "start to normalize"
	for i in range(len(dt)):
		M = max(dt[i])
		m = min(dt[i])
		if M!=m:
			dt[i] = [(j-m)/(M-m) for j in dt[i]]
		else:
			dt[i] = [0 for j in dt[i]]
	print "start to zip"
	d = zip(*dt)
	return d
	
"""
----------------------------------------------
	DimensionalityReduction
	Description:use PCA to reduce the dimension of dataset and print eigenvalue & eigenvector to isolate files.
	Input: d(dataset), d_eigenvalue(default empty), d_eigenvector(default empty)
	Output: d_eigenvalue_total(total sum of all items in d_eigenvalue), two isolate files
----------------------------------------------
"""
	
def DimensionalityReduction(d, eigenvalue_filename, eigenvector_filename):
	print "start to PCA"
	d_pca = pca(np.array(d))
	d_eigenvalue = [i[0] for i in d_pca]
	d_eigenvector = [i[1] for i in d_pca]

	#global eigenvector_filename
	eigenvector_output = open(eigenvector_filename,'w')
	for i in range(len(d_eigenvector)):
		for j in range(len(d_eigenvector[i])):
			eigenvector_output.write(str(d_eigenvector[i][j])+"\t")
		eigenvector_output.write("\n")
	eigenvector_output.close()
	
	#global d_eigenvalue_sum, d_eigenvalue_total

	#global eigenvalue_filename
	eigenvalue_output = open(eigenvalue_filename,'w')
	d_eigenvalue_total = 0.0
	for i in range(len(d_eigenvalue)):
		d_eigenvalue_total += d_eigenvalue[i]
	d_eigenvalue_sum = 0.0
	for i in range(len(d_eigenvalue)):
		d_eigenvalue_sum += d_eigenvalue[i]/d_eigenvalue_total
		print >> eigenvalue_output, d_eigenvalue[i]/d_eigenvalue_total, "\t", d_eigenvalue_sum
	eigenvalue_output.close()
	return d_eigenvalue, d_eigenvector, d_eigenvalue_total
	
"""
----------------------------------------------
	PrintClusteringResult
	Description: print total clustering results to external file.
	Input: c1 (c1[i][0] is the clustering result for i-th instances)
	Output: the external file 'cluster(DAP)' to store clustering results of total instances
----------------------------------------------
"""
	
def PrintClusteringResult(cluster_filename, c1):
	#global cluster_filename
	print "Printing Cluster(DAP)"
	f = open(cluster_filename,'w')
	for i in range(len(c1)):
		if i!=0:
			f.write('\n')
		f.write(str(c1[i][0]))
	f.close()
	return 0
	
#========================================

#main component

#========================================

def main(input_json_filename):

	dataset_filename, eigenvalue_sum_threshold, Pinit, eigenvalue_filename, eigenvector_filename, cluster_filename = InputData(input_json_filename)
	# decoded['dataset_filename'], decoded['eigenvalue_sum_threshold'], decoded['Pinit'], decoded['eigenvalue_filename'], decoded['eigenvector_filename'], decoded['cluster_filename']
	eigenvalue_sum_threshold = float(eigenvalue_sum_threshold)
	Pinit = int(Pinit)

	print "start read dataset"
	d = read_dataset(dataset_filename,'\t')
	print "end of read_dataset"

	d = ConvertDataFormat(d)
	
	print type(d[0][0])
	d = DatasetNormalization(d)

	d_eigenvalue, d_eigenvector, d_eigenvalue_total = DimensionalityReduction(d, eigenvalue_filename, eigenvector_filename)

	C=[]
	counter = []
	flag_counter = []
	value_counter = []

	print "start to DAP"

	d_eigenvalue_sum = 0.0
	for component in range(len(d_eigenvector)):
		print "component = ",component
		d_eigenvalue_sum += d_eigenvalue[component]/d_eigenvalue_total
		print "d_eigenvalue_sum = ",d_eigenvalue_sum
		if d_eigenvalue_sum > eigenvalue_sum_threshold:
			pass
		else:
			continue
		trans_matrix = np.array(zip(*d_eigenvector[0:component+1]))
		d_transf = trans_matrix.T.dot(np.array(d).T).T

		if component <2:
			d_transf = [[round(j,2) for j in i] for i in d_transf]
		else:
			d_transf = [[round(j,1) for j in i] for i in d_transf]
		numeric_list = range(0,component+1)
		nominal_list = range(0,0)
	
		c1,c2,data_ch,data_cluster,S = DAP(d_transf,numeric_list,nominal_list,Pinit)
		print data_cluster
		C.append(c1)
	#print "max_cluster_number = ",find_max(c1)
		break

	PrintClusteringResult(cluster_filename, c1)
	print "max = ",find_max(c1)
	return c1

if __name__ == "__main__":
	main(sys.argv[1])