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
	Description: read the dataset from json data
	Input:	N/A
	Output:	N/A
----------------------------------------------
"""

def Initialization(input_json_filename):
	if input_json_filename.__len__() == 0:
		print "python [python's filename] [json's filename]"
		exit()
	FILE = open(input_json_filename,"rU")
	rawdata = FILE.read()
	decoded = json.loads(rawdata)
	FILE.close()
	return decoded
	
def InputData(decoded):
	#global d
	#global eigenvalue_sum_threshold, Pinit
	#global eigenvalue_filename, eigenvector_filename, cluster_filename
	
	print decoded['dataset_filename']
	print decoded['eigenvalue_sum_threshold']
	print decoded['Pinit']

	if decoded.has_key('eigenvalue_filename') == True:
		print decoded['eigenvalue_filename']
	else:
		print 'empty eigenvalue_filename'
		decoded['eigenvalue_filename'] = ""
	
	if decoded.has_key('eigenvector_filename') == True:
		print decoded['eigenvector_filename']
	else:
		print 'empty eigenvector_filename'
		decoded['eigenvector_filename']

	if decoded.has_key('cluster_filename') == True:
		print decoded['cluster_filename']
	else:
		print 'empty cluster_filename'
		decoded['cluster_filename'] = ""

	#Pinit = int(decoded['Pinit'])
	#eigenvalue_sum_threshold = float(decoded['eigenvalue_sum_threshold'])
	#eigenvector_filename = copy.deepcopy(decoded['eigenvector_filename'])
	#eigenvalue_filename = copy.deepcopy(decoded['eigenvalue_filename'])
	#cluster_filename = copy.deepcopy(decoded['cluster_filename'])
	return decoded['dataset_filename'], decoded['eigenvalue_sum_threshold'], decoded['Pinit'], decoded['eigenvalue_filename'], decoded['eigenvector_filename'], decoded['cluster_filename']
	


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

	if eigenvector_filename.__len__() != 0:
		#there exits an eigenvector filename
		eigenvector_output = open(eigenvector_filename,'w')
		for i in range(len(d_eigenvector)):
			for j in range(len(d_eigenvector[i])):
				eigenvector_output.write(str(d_eigenvector[i][j])+"\t")
			eigenvector_output.write("\n")
		eigenvector_output.close()
	else:
		#this is an empty eigenvector filename
		pass

	eigenvalue_output = open(eigenvalue_filename,'w')
	if eigenvalue_filename.__len__() != 0:
		#there exists an eigenvalue filename
		d_eigenvalue_total = 0.0
		for i in range(len(d_eigenvalue)):
			d_eigenvalue_total += d_eigenvalue[i]
		d_eigenvalue_sum = 0.0
		for i in range(len(d_eigenvalue)):
			d_eigenvalue_sum += d_eigenvalue[i]/d_eigenvalue_total
			print >> eigenvalue_output, d_eigenvalue[i]/d_eigenvalue_total, "\t", d_eigenvalue_sum
		eigenvalue_output.close()
	else:
		#this is an empty eigenvalue filename
		pass

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
	if cluster_filename.__len__() == 0:
		print "no need to print external file"
		return 0
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

def main(decoded):

	dataset_filename, eigenvalue_sum_threshold, Pinit, eigenvalue_filename, eigenvector_filename, cluster_filename = InputData(decoded)
	# decoded['dataset_filename'], decoded['eigenvalue_sum_threshold'], decoded['Pinit'], decoded['eigenvalue_filename'], decoded['eigenvector_filename'], decoded['cluster_filename']
	eigenvalue_sum_threshold = float(eigenvalue_sum_threshold)
	Pinit = int(Pinit)

	print "start read dataset"
	d = read_dataset(dataset_filename,'\t')
	print "end of read_dataset"
	d = Convert2FloatArray(d,2)
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
	decoded = Initialization(sys.argv[1])
	main(decoded)