from math import log
from collections import Counter
from AP import *

"""
----------------------------------------------
	ConvertDataFormat
	Description: Convert dataset into real number format 
	Steps: 1. convert 'on' 'off' 'stand' into real number(this is specially for BL313) 2. 
	Input: d(dataset)
	Output: 0 for success, 1 for some error
----------------------------------------------
"""
	
def Convert2FloatArray(d, array):
	print "start to convert to float"
	if array == 1:
		for i in range(len(d)):
			if 'on' in d[i]:
				d[i] = 1
			elif 'off' in d[i]:
				d[i] = 0
			elif 'stand' in d[i]:
				d[i] = 0.1
		d = [float(i) for i in d]
		
	if array == 2:
		for i in range(len(d)):
			if d[i][len(d[i])-1] == '\r':
				d[i] = d[i][:-1]
			for j in range(len(d[i])):
				if 'on' in d[i][j]:
					d[i][j] = 1
				elif 'off' in d[i][j]:
					d[i][j] = 0
				elif 'stand' in d[i][j]:
					d[i][j] = 0.1
		d = [[float(j) for j in i] for i in d]
		
	print 'start to convert to float...done...'
	return d


def entropy(Alphabet):
	H = 0
	P=[]
	Number_of_Alphabet = float(len(Alphabet))
	Counter_of_Alphabet = Counter(Alphabet)
	for element in list(Counter_of_Alphabet):
		p = Counter_of_Alphabet[element]/Number_of_Alphabet #Normalization
		P.append(p)
		H = H+ -1*p*log(p,2)
	return H

def read_dataset(File_Name, Split_Symbol):
	f = open(File_Name,'rU')
	data = f.read()
	data = data.split('\n')
	line = data.__len__()
	if line != 1:
		while len(data[data.__len__()-1]) == 0:
			data = data[:-1]
			line -= 1
	for i in range(len(data)):
		data[i] = data[i].split(Split_Symbol)
		if data[i][len(data[i])-1] == '':
			data[i] = data[i][:-1]
	#print "data[0]=",data[0]
	f.close()
	return data, line

def median(Q):
	Q = sorted(Q)
	l = len(Q)
	if l%2 == 0:
		return 0.5*(Q[l/2-1]+Q[l/2+1-1])
	else:
		return Q[(l+1)/2-1]


def s1(data,numeric_list,nominal_list,Pinit):

	#input: data, numeric_list, nominal_list, P_init[0:median,1:minimal]
	feature = zip(*data)
	S = []
	print "len numeric_list = ",len(numeric_list)
	for n in numeric_list:
		#Normalizing
	#	print "feature[n] = ",feature[n]
		feature[n] = [float(f_index) for f_index in feature[n] ]
		Min = min(feature[n])
		Max = max(feature[n])
		try:
			feature[n] = sorted([(f_index - Min)/(Max - Min) for f_index in feature[n] ])
		except:
			pass
		#	print "Min Max ",Min," ",Max
		#	while True:
		#		pass

		x = Counter(feature[n])
		xx = sorted(list(x))
		s = [[0 for i in range(len(list(x)))] for j in range(len(list(x)))]
		#Computing Similarity Matrix of feature(n)
		#P_init = median(list(x))
		if Pinit == 0:
			P_init = median(list(x))
		else:
			P_init = max(list(x))
		n_max = x.most_common()[0][1]
	#	print "sizeof x",len(x)
		for i in range(len(list(x))):
			for j in range(len(list(x))):
				if i != j:
					s[i][j] = (-1) * abs(xx[i] - xx[j])
				else:
					s[i][j] = (-1) * P_init * (float(n_max)-float(x[xx[i]])+1.0) / (float(n_max)+1.0)
		S.append(s)

	for n in nominal_list:

		x = Counter(feature[n])
	#	print "len x = ",len(x)

		s = [[0 for i in range(len(list(x)))] for j in range(len(list(x)))]
		P_init = 0.5
		n_max = x.most_common()[0][1]
		for i in range(len(list(x))):
			for j in range(len(list(x))):
				if i != j:
					if list(x)[i] != list(x)[j]:
						s[i][j] = -1
					else:
						s[i][j] = 0
				else:
					s[i][j] = (-1) * P_init * (float(n_max)-float(x[list(x)[i]])+1.0) / (float(n_max)+1.0)
		S.append(s)
	print "len S=",len(S)
	return S

def s3(data,cluster,numeric_list,nominal_list,Pinit):
	cluster_result = []
	X = []

	source_feature = zip(*data)
	feature = source_feature
	final_feature = source_feature
	cluster = [[ str(j) for j in i] for i in cluster]

	for n in numeric_list:
		#Normalizing
		feature[n] = [float(f_index) for f_index in source_feature[n] ]
		Min = min(feature[n])
		Max = max(feature[n])
		try:
			feature[n] = [(f_index - Min)/(Max - Min) for f_index in feature[n] ]
		except:
			pass
		x = Counter(feature[n])
		xx = sorted(list(x))
		X = X + [xx]
#	print "x = ",x
#	print "xx = ",xx
#	print "X = ",X
#	print cluster

	cluster_result = [sorted([(X[i][j],cluster[i][j]) for j in range(len(X[i]))]) for i in range(len(X))]
	# X[i][j] is the j-th unique value in Feature[i]
	# cluster[i][j] is the index of ClusterHead for X[i][j]
#	print "cluster result = ",cluster_result


	for n in numeric_list:
		feature[n] = [float(f_index) for f_index in source_feature[n] ]
		Min = min(feature[n])
		Max = max(feature[n])
		try:
			feature[n] = [str((f_index - Min)/(Max - Min)) for f_index in feature[n] ]
		except:
			pass
		temp_X = [str(x_index) for x_index in X[n]]
		for i in range(len(feature[n])):
			if feature[n][i]=="-0.0":
				feature[n][i] = "0.0"
			try:
				final_index = temp_X.index(str(feature[n][i]))
			except:
				print "temp_X ",temp_X
				print "feature[n][i] ",feature[n][i]
			# find index of i-th data in feature[n] in X[n]
			# final_feature[n][i] is dealing with all data from source_feature
			final_feature[n][i] = cluster[n][final_index]
			# replace the value of i-th data in feature[n] as the index of its cluster head in unique value

#	print "final_feature = ",final_feature
#	print "final_index = ",final_index
#	print X[0][final_index]
#	print "X = ",X
#	print "xx = ",xx

	extrected_feature = zip(* final_feature)
	extrected_feature = extrected_feature

	extrected_feature = zip(* final_feature)
#	print "final_feature",final_feature[0][0]
#	print "extrected_feature",extrected_feature[0][0]
	extrected_feature_string = [str(ex_index).replace('(','').replace(')','').replace('\'','').replace(' ','') for ex_index in extrected_feature]
	count_e_feature = Counter(extrected_feature_string)
#	print "extrected_feature_string",extrected_feature_string[0]
#	print count_e_feature
	# create a collection of unique combination of ClusterHead index in each Feature by counter
	list_e_feature = list(count_e_feature)
	# list_e_feature is a list of unique combination of ClusterHead index in each Feature

#	print "extrected_feature_string = ",extrected_feature_string
#	print "count_e_feature = ",count_e_feature
#	print "list_e_feature = ",list_e_feature
#	print "extrected_feature = ",extrected_feature


	Simi = []
	Min = 1000
	Max = -1000
	n_max = count_e_feature.most_common()[0][1]

	for i in range(len(list_e_feature)):
		D = []
		for j in range(len(list_e_feature)):
			d = 0
			if i !=j:
				list_i = list_e_feature[i].split(',')
				list_j = list_e_feature[j].split(',')
				# split i-th element and j-th element, where each element is a unique combination of the index of ClusterHead in each Feature
				for n in numeric_list:
					d = d + abs(X[n][int(list_i[n])] - X[n][int(list_j[n])])
					# list_i[n] is the clusterhead index of the i-th data in feature[n]
				for n in nominal_list:
					#if list_i[n] == list_j[n]:
					if list_i[n] != list_j[n]:
						d = d + 1
				if d > Max:
					Max = d
					# update maximum distance
				if d < Min:
					Min = d
					# update minimum distance
			D.append(d)
		Simi.append(D)

	self_preference=[]

	# Create Similarity Matrix for unique combination of ClusterHead in each Feature
	for i in range(len(list_e_feature)):
		for j in range(len(list_e_feature)):
			if i != j:
				# Normalization
				Simi[i][j] = (-1) * float(Simi[i][j])/float(Max)
				if i>j:
					self_preference.append(Simi[i][j])

	if Pinit == 0:
		preference_median = median(self_preference)
	else:
		preference_median = min(self_preference)

	for i in range(len(list_e_feature)):
		Simi[i][i] = preference_median * (float(n_max)-float(count_e_feature[list_e_feature [i]]) + 1.0) / (float(n_max)+1.0)

	return Simi,extrected_feature

def s4(data,cluster,cluster_final,numeric_list,nominal_list):
	cluster_result = []
	X = []

	source_feature = zip(*data)
	feature = source_feature
	final_feature = source_feature
	cluster = [[ str(j) for j in i] for i in cluster]
	cluster_final = [str(i) for i in cluster_final]

	for n in numeric_list:
		#Normalizing
		feature[n] = [float(f_index) for f_index in source_feature[n] ]
		Min = min(feature[n])
		Max = max(feature[n])
		try:
			feature[n] = [(f_index - Min)/(Max - Min) for f_index in feature[n] ]
		except:
			pass
		x = Counter(feature[n])
		xx = sorted(list(x))
		X = X + [xx]

	cluster_result = [sorted([(X[i][j],cluster[i][j]) for j in range(len(X[i]))]) for i in range(len(X))]
	# X[i][j] is the j-th unique value in Feature[i]
	# cluster[i][j] is the index_of_ClusterHead for X[i][j]

#	print "feature1 = ",feature

	for n in numeric_list:
		feature[n] = [float(f_index) for f_index in source_feature[n] ]
		Min = min(feature[n])
		Max = max(feature[n])
		try:
			feature[n] = [str((f_index - Min)/(Max - Min)) for f_index in feature[n] ]
		except:
			pass
		temp_X = [str(x_index) for x_index in X[n]]
		for i in range(len(feature[n])):
			#	updated in 2015.11.05
			if feature[n][i]=="-0.0":
				feature[n][i] = "0.0"
			try:
				final_index = temp_X.index(feature[n][i])
			except:
				final_index = temp_X.index(str(feature[n][i]))
			# find index of i-th data in feature[n] in X[n]

			final_feature[n][i] = cluster[n][final_index]
			# replace the value of i-th data in feature[n] as the index of its cluster head

	extrected_feature = zip(* final_feature)

#	final feature (location add all)
	extrected_feature_string = [str(ex_index).replace('(','').replace(')','').replace('\'','').replace(' ','') for ex_index in extrected_feature]
	count_e_feature = Counter(extrected_feature_string)
	list_e_feature = list(count_e_feature)
	# list_e_feature is a list of unique combination of ClusterHead in each Feature
	Simi = []
	Min = 1000
	Max = -1000
	n_max = count_e_feature.most_common()[0][1]
	for i in range(len(list_e_feature)):
		D = []
		for j in range(len(list_e_feature)):
			d = 0
			if i !=j:
				list_i = list_e_feature[i].split(',')
				list_j = list_e_feature[j].split(',')
				for n in numeric_list:
					d = d + abs(X[n][int(list_i[n])] - X[n][int(list_j[n])])
				for n in nominal_list:
					if list_i[n] == list_j[n]:
						d = d + 1
				if d > Max:
					Max = d
				if d < Min:
					Min = d
			else:
				d = (-1) * 0.5 * (float(n_max)-float(count_e_feature[list_e_feature [i]])+1.0) / (float(n_max)+1.0)
			D = D +[d]
		Simi = Simi + [D]

	for i in range(len(list_e_feature)):
		for j in range(len(list_e_feature)):
			if i != j:
				try:
					Simi[i][j] = (-1) *(Simi[i][j] - Min)/(Max - Min)
				except:
					Simi[i][j] = (-1) * (Simi[i][j])
					

	latest_feature = zip(*feature)

	Final = []
	#cluster_final = [1010, 1072, 921, 368, 1862, 730, 1072, 1692, 951, 569, 1406, 1072, 1692, 1692, 368, 381, 834, 1692, 1692, 1248, 1692, 1692, 1692, 1795, 2105, 1248, 1692, 1010, 1795, 1692, 730, 1163, 1287, 1858, 2105, 1010, 1795, 1072, 834, 1059, 730, 1692, 1040, 1692, 1248, 2088, 1692, 2088, 834, 1010, 2105, 1040, 1287, 1059, 1163, 1040, 2105, 368, 834, 2088, 557, 2088, 730, 1862, 1795, 1406, 1795, 1692, 1010, 414, 1040, 1692, 1287, 1692, 498, 2105, 2088, 2088, 1248, 368, 381, 1406, 834, 1692, 368, 1248, 569, 557, 498, 1163, 1040, 557, 951, 2088, 368, 1072, 2105, 1417, 951, 834, 1163, 1795, 1858, 368, 1287, 951, 834, 569, 1163, 1040, 1059, 1059, 1248, 1406, 414, 921, 1692, 2105, 557, 1417, 1406, 1040, 2105, 557, 1287, 2105, 1040, 1040, 834, 130, 1059, 2088, 2105, 569, 1795, 730, 730, 1858, 1795, 1692, 1692, 1059, 1040, 951, 1059, 498, 1059, 2088, 951, 730, 1040, 569, 1692, 1010, 1692, 1692, 381, 569, 1040, 1248, 730, 1248, 1692, 2105, 1406, 2088, 1059, 381, 1692, 2088, 1858, 1692, 557, 1692, 1795, 1040, 1862, 1692, 2088, 1248, 1692, 498, 2105, 1692, 1163, 1692, 834, 1059, 1692, 1795, 1417, 1692, 1040, 730, 1040, 834, 2088, 1163, 1692, 2105, 730, 1010, 414, 1406, 951, 557, 2088, 834, 1287, 1040, 921, 557, 1692, 1248, 1072, 1795, 834, 730, 1692, 1858, 1692, 368, 2105, 1692, 1692, 1692, 951, 381, 2105, 1406, 368, 498, 951, 1248, 2105, 1692, 2105, 2088, 1072, 1692, 2105, 498, 1692, 1040, 951, 1040, 1059, 1059, 569, 1059, 1692, 2088, 1692, 1059, 1692, 381, 2088, 834, 1040, 1040, 2088, 1406, 1692, 498, 2088, 1692, 414, 1059, 2088, 1010, 414, 1040, 1692, 1858, 1040, 1692, 1040, 1417, 1858, 2105, 834, 557, 1692, 1692, 1163, 1040, 730, 1692, 1361, 2105, 2088, 2088, 1040, 569, 1287, 1040, 1072, 1692, 730, 1692, 2105, 1059, 1072, 1040, 1692, 368, 1692, 951, 1059, 1361, 834, 1287, 834, 1406, 1417, 1163, 414, 1163, 1040, 569, 2088, 498, 1692, 569, 557, 730, 730, 1040, 1287, 1040, 951, 2088, 1692, 1406, 1692, 1072, 368, 557, 1417, 381, 1417, 730, 730, 1858, 1059, 1417, 1059, 2105, 368, 1163, 1040, 951, 1072, 1248, 730, 1692, 1248, 951, 1059, 2088, 2088, 1692, 1692, 1072, 381, 1248, 1692, 368, 1059, 951, 1795, 557, 1692, 1692, 2088, 414, 368, 1692, 1361, 1692, 381, 1692, 1010, 1692, 921, 557, 1692, 834, 1858, 730, 1862, 1072, 1059, 921, 1059, 1862, 557, 1059, 1858, 730, 1406, 2088, 1010, 498, 405, 498, 1858, 1692, 1795, 2088, 2105, 1361, 1417, 414, 1072, 1072, 1692, 2088, 1059, 2088, 1692, 2088, 2088, 921, 1858, 1692, 368, 381, 1692, 1040, 1059, 1692, 1692, 569, 1163, 730, 1248, 368, 1417, 951, 2088, 1692, 1417, 1692, 1040, 1858, 1692, 921, 1248, 1692, 1692, 1692, 1059, 1163, 1692, 2088, 1692, 2105, 557, 381, 2088, 1163, 1040, 1417, 1692, 730, 405, 951, 1692, 1287, 2088, 730, 2088, 1692, 569, 834, 2105, 557, 569, 1040, 921, 405, 1692, 1692, 1248, 1692, 1059, 921, 368, 951, 1287, 557, 834, 1692, 2105, 1406, 1692, 498, 1287, 498, 834, 2088, 2088, 1287, 1692, 1287, 1692, 1248, 1287, 2088, 730, 2105, 1010, 1010, 1163, 1072, 1059, 834, 1692, 1040, 1040, 951, 405, 2088, 2088, 2088, 1040, 1692, 1692, 951, 1040, 1858, 368, 1040, 1692, 730, 498, 1858, 834, 2088, 1040, 381, 1040, 834, 1692, 414, 498, 1040, 1072, 1059, 1059, 1692, 1059, 1417, 1040, 1406, 557, 1248, 1692, 414, 1692, 2088, 368, 1072, 498, 1040, 1692, 1248, 569, 921, 2088, 1040, 1692, 730, 1248, 1406, 921, 1858, 1417, 1248, 381, 1862, 1862, 2105, 569, 1692, 951, 1072, 1059, 1040, 1287, 1040, 1059, 1010, 1040, 1040, 1692, 1072, 1059, 1248, 405, 1692, 730, 1059, 1692, 1692, 1692, 1040, 1040, 1040, 2088, 730, 1692, 1040, 1692, 1072, 921, 1795, 1858, 1010, 1692, 1040, 1059, 2088, 1059, 569, 1692, 834, 1692, 921, 1692, 1692, 1059, 921, 1059, 921, 1248, 1040, 1059, 569, 1858, 1692, 368, 2105, 834, 1692, 1059, 498, 1862, 1072, 2105, 1072, 2088, 921, 1692, 381, 1692, 1858, 1163, 381, 368, 1361, 834, 921, 951, 730, 921, 1692, 2088, 569, 1692, 368, 405, 1858, 1692, 1406, 2088, 951, 1858, 1795, 368, 1406, 1692, 1040, 498, 951, 557, 1858, 1040, 2088, 1059, 951, 1692, 1692, 1059, 368, 1059, 1163, 1040, 1692, 951, 381, 2088, 1059, 1072, 2088, 1059, 1040, 1692, 1692, 1692, 1692, 1287, 557, 498, 730, 1059, 1406, 1059, 1040, 498, 1692, 1040, 2105, 557, 381, 1692, 1795, 921, 730, 921, 2088, 405, 1692, 921, 381, 834, 368, 1040, 1692, 1862, 1862, 557, 1692, 730, 2105, 569, 2088, 1692, 1417, 1692, 1417, 1040, 2105, 2105, 1248, 381, 1059, 569, 1072, 1692, 381, 405, 1059, 405, 1862, 1862, 557, 557, 730, 1692, 1692, 1692, 730, 921, 1692, 951, 2088, 1059, 834, 1692, 921, 2088, 1040, 1692, 834, 1692, 1248, 1040, 1248, 1010, 921, 730, 1692, 1417, 1795, 1287, 1248, 1059, 1361, 1862, 1795, 730, 557, 1072, 2088, 921, 368, 1040, 1059, 1059, 1692, 1692, 2088, 1072, 1010, 557, 921, 730, 1010, 1040, 1692, 569, 2088, 1406, 834, 498, 921, 1692, 921, 1858, 1072, 1072, 834, 1692, 1248, 1692, 1862, 1862, 1692, 1248, 2088, 1406, 1858, 1692, 1072, 414, 1040, 1862, 1862, 1858, 569, 2088, 730, 730, 1692, 834, 1059, 1040, 2088, 1858, 2088, 1692, 557, 1692, 1692, 730, 569, 921, 951, 1040, 1248, 1406, 557, 951, 1862, 921, 1059, 1692, 921, 2088, 2105, 498, 1040, 1692, 730, 1692, 1692, 1692, 1248, 1040, 2105, 1010, 1406, 951, 1072, 1287, 1040, 414, 1858, 569, 1692, 1406, 1417, 951, 1040, 2088, 2088, 1040, 1059, 1692, 557, 1795, 498, 921, 498, 1059, 1059, 405, 1287, 921, 414, 1072, 1858, 1692, 2105, 381, 557, 498, 2088, 381, 1040, 730, 730, 1692, 1858, 730, 730, 2088, 1692, 2088, 1417, 557, 1692, 1040, 1072, 1406, 1361, 1862, 2105, 951, 405, 1059, 2088, 1406, 1692, 1072, 1692, 1163, 569, 1248, 1692, 498, 1692, 730, 1287, 1858, 730, 730, 557, 1059, 730, 381, 1040, 405, 1795, 1692, 951, 1692, 1417, 921, 1072, 1862, 1072, 557, 1692, 921, 2105, 1040, 1858, 1040, 730, 2088, 1040, 1692, 996, 414, 730, 1795, 1795, 2088, 1059, 921, 951, 951, 368, 1072, 1692, 1692, 1010, 1040, 1858, 2088, 1858, 1858, 381, 1059, 951, 1059, 834, 1163, 1692, 2105, 2088, 951, 368, 1040, 921, 1040, 1059, 1862, 730, 730, 1692, 1692, 498, 498, 951, 1692, 1040, 1692, 2088, 1692, 1040, 2088, 1406, 557, 1010, 951, 1692, 2088, 368, 2105, 1072, 557, 2105, 1059, 2105, 1059, 1692, 921, 1163, 1248, 557, 1406, 1040, 1248, 1692, 405, 569, 569, 1072, 1858, 1040, 1862, 951, 1163, 834, 1163, 1040, 1248, 730, 1059, 1406, 1417, 1059, 1010, 1163, 1059, 951, 1692, 569, 730, 1692, 498, 834, 1040, 405, 951, 1163, 569, 1248, 1059, 2088, 2105, 1692, 1072, 1692, 381, 1248, 951, 1248, 1361, 569, 1040, 951, 730, 1059, 2105, 405, 834, 1692, 1692, 730, 834, 368, 1692, 1072, 1862, 1692, 921, 498, 368, 569, 834, 2088, 1692, 368, 2105, 557, 1040, 951, 1072, 1692, 951, 2088, 1010, 381, 1287, 1858, 1248, 498, 2088, 1163, 1692, 2105, 1059, 1059, 730, 1248, 834, 921, 1163, 1692, 2088, 1692, 1072, 1059, 1406, 2088, 2088, 2105, 1072, 1417, 834, 1163, 381, 569, 1692, 1692, 1040, 951, 1040, 1692, 834, 730, 1059, 1040, 730, 1862, 368, 834, 1059, 1858, 1692, 730, 1692, 1692, 557, 1692, 2088, 1862, 2088, 730, 1692, 557, 2088, 569, 414, 921, 921, 1010, 569, 1163, 1692, 1216, 381, 1361, 557, 2088, 2088, 498, 1287, 1040, 1010, 730, 951, 405, 2088, 1072, 1692, 557, 1692, 730, 1862, 921, 405, 381, 1692, 2088, 381, 368, 1406, 381, 2088, 1692, 2088, 1248, 834, 1248, 2088, 834, 1692, 1692, 1059, 1059, 1858, 569, 1692, 1692, 1248, 1692, 1692, 1040, 1072, 730, 921, 1248, 1287, 1059, 1248, 730, 1417, 921, 2088, 2105, 1287, 2088, 1862, 2088, 1040, 730, 921, 1692, 730, 1248, 1287, 1862, 1010, 1862, 1692, 1692, 1692, 1862, 1072, 1248, 2088, 1059, 1287, 1692, 1858, 1287, 381, 1692, 1795, 1248, 368, 1040, 498, 368, 368, 1406, 1287, 730, 1040, 2105, 921, 1010, 2088, 2105, 2105, 405, 557, 1072, 1692, 1248, 1692, 2088, 730, 1862, 1417, 368, 2088, 1692, 730, 1692, 557, 368, 368, 2105, 2088, 2088, 730, 730, 1692, 1059, 1059, 730, 1059, 1692, 834, 1692, 1010, 569, 1692, 1862, 921, 1692, 1059, 368, 1361, 1059, 1692, 381, 730, 730, 730, 1059, 2088, 1040, 1163, 2105, 1072, 1248, 1040, 557, 1059, 557, 951, 730, 1406, 569, 2088, 1692, 1040, 1406, 730, 1287, 405, 1692, 834, 1692, 1010, 2088, 1692, 1692, 557, 381, 557, 834, 557, 1059, 1040, 1692, 1858, 1406, 2088, 405, 368, 834, 1692, 921, 1692, 557, 2088, 1692, 1417, 1858, 2105, 1040, 1059, 834, 834, 1795, 921, 1072, 2105, 1795, 730, 1072, 1040, 1795, 1040, 1795, 921, 951, 2088, 1858, 1692, 730, 1692, 834, 1010, 1040, 569, 569, 1858, 2088, 1040, 2105, 1692, 1248, 1417, 368, 1010, 1858, 1692, 498, 1040, 1059, 1692, 1692, 1862, 1248, 569, 1248, 1692, 2105, 498, 730, 1692, 1287, 1692, 1862, 1406, 368, 1287, 1692, 951, 1010, 1248, 1692, 730, 405, 921, 1692, 1692, 1692, 1287, 1858, 1862, 1248, 730, 1692, 414, 1692, 1406, 1692, 834, 1692, 2088, 2105, 1059, 1862, 1692, 414, 1059, 730, 557, 1248, 1406, 1163, 569, 368, 951, 1692, 1248, 1361, 1406, 1858, 1692, 1059, 1406, 2105, 1417, 2088, 1692, 2088, 730, 730, 405, 1059, 921, 1692, 1862, 921, 730, 1692, 730, 1692, 557, 1248, 1417, 1040, 1692, 1072, 730, 1692, 2088, 1417, 2088, 1406, 405, 2105, 2105, 2088, 1040, 2105, 1692, 2105, 921, 1692, 557, 414, 1417, 414, 1692, 834, 2088, 1059, 921, 1692, 557, 1795, 557, 951, 2088, 1692, 2105, 1072, 368, 414, 1692, 921, 1248, 557, 1248, 381, 1040, 921, 834, 951, 368, 1059, 834, 2105, 557, 557, 951, 1072, 1692, 2105, 1059, 1059, 1692, 557, 1287, 1692, 1692, 1248, 414, 1862, 730, 1059, 1040, 1692, 1059, 1858, 2105, 1059, 1163, 951, 1059, 1059, 1072, 2088, 1692, 1858, 557, 921, 730, 1417, 1163, 1692, 1417, 1692, 2088, 1692, 1163, 1406, 2105, 2088, 1692, 951, 1692, 1692, 1040, 1692, 1406, 1072, 1163, 951, 730, 1287, 921, 1072, 730, 1417, 1248, 1692, 1040, 1692, 569, 730, 1692, 1692, 1692, 2088, 951, 921, 1692, 1858, 1692, 2105, 1692, 1406, 2105, 1417, 1692, 1692, 2105, 381, 1040, 1040, 1858, 368, 730, 730, 498, 414, 1248, 1692, 951, 381, 951, 2088, 2088, 834, 730, 1040, 1692, 1287, 1692, 1059, 951, 368, 1361, 1795, 1692, 921, 1040, 1059, 569, 1692, 730, 368, 2105, 1692, 2088, 1692, 1010, 414, 834, 2088, 498, 1059, 2105, 2105, 498, 1692, 1040, 1858, 1692, 1692, 1692, 381, 381, 1692, 951, 414, 1059, 1040, 1361, 921, 951, 1406, 2105, 405, 1858, 1287, 1040, 381, 1040, 1163, 1072, 1858, 368, 1692, 498, 921, 1692, 1692, 557, 2088, 834, 368, 730, 1072, 1059, 951, 834, 1692, 1417, 405, 569, 1040, 1040, 1858, 951, 1059, 951, 730, 2088, 921, 1040, 1692, 414, 834, 2105, 2088, 2105, 368, 2088, 1287, 1795, 381, 1692, 1040, 1072, 921, 921, 1417, 1059, 1248, 1692, 1072, 2088, 1040, 730, 1858, 569, 951, 1692, 557, 1287, 1248, 1072, 569, 1858, 381, 1248, 1862, 2088, 1059, 1858, 1795, 1072, 569, 1059, 1040, 1692, 1692, 2105, 1406, 1059, 1692, 2105, 569, 1040, 951, 1417, 1692, 368, 1692, 414, 2105, 498, 1040, 1163, 368, 1072, 557, 834, 1059, 498, 1406, 730, 1858, 730, 1417, 569, 1862, 1287, 1692, 405, 405, 368, 921, 381, 1040, 2088, 1163, 2088, 1040, 1040, 1010, 1692, 1692, 1795, 1795, 834, 1248, 1248, 1010, 1010, 921, 1059, 569, 1692, 921, 1692, 2088, 1862, 2105, 1072, 1040, 557, 1059, 557, 1858, 557, 2088, 1040, 405, 1040, 1692, 1059, 569, 2088, 730, 1692, 1059, 1040, 1072, 834, 730, 569, 1059, 730, 834, 921, 1040, 1692, 1248, 921, 1858, 1692, 1692, 1059, 1692, 368, 1692, 1040, 405, 1406, 1248, 730, 1692, 1072, 381, 1692, 834, 1692, 1692, 2088, 1692, 1692, 1059, 368, 2105, 414, 1692, 730, 1692, 1059, 1059, 381, 1692, 1692, 730, 1072, 921, 1040, 1692, 1040, 1692, 498, 921, 1059, 1163, 1795, 1040, 1059, 1040, 1010, 2088, 1862, 1040, 569, 1862, 1287, 1858, 498, 1692, 1059, 381, 1040, 951, 1692, 1692, 1692, 1692, 1417, 1692, 1248, 557, 2088, 2088, 1040, 381, 1692, 2088, 1692, 1072, 834, 1692, 1072, 2105, 730, 1406, 2088, 1692, 1040, 1248, 1072, 1072, 921, 951, 368, 1163, 921, 1406, 1248, 1059, 921, 2026, 834, 1059, 1059, 730, 1692, 1163, 1858, 498, 1795, 557, 1248, 2088, 1040, 569, 1059, 569, 557, 1795, 1692, 730, 951, 834, 730, 1040, 1040, 951, 414, 951, 1059, 1040, 1010, 1163, 1692, 730, 2105, 498, 569, 1040, 1858, 951, 1406, 2105, 730, 834, 2088, 1692, 1692, 381, 1692, 381, 1417, 1010, 951, 1692, 557, 1862, 2088, 2088, 1795, 1692, 1010, 2088, 2105, 1692, 1692, 1692, 730, 1692, 1040, 1692, 498, 1248, 498, 921, 1692, 1040, 1010, 921, 2105, 1248, 557, 569, 569]

	new_data = []
	new_data2 = []
	#print "len(data) = ",len(data)
	for i in range(len(data)):
		new_point = []
		new_point2 = []
	#	print "pattern = ",latest_feature[i]
		pattern = str(latest_feature[i]).replace(' ','').replace('\'','').replace('(','').replace(')','')
	#	print "pattern = ",pattern
	#	print "list_e_feature = ",list_e_feature
		cluster_index = list_e_feature.index(pattern)
		cluster_final_header = cluster_final[cluster_index]
		new_point = [cluster_final_header] + [data[i]]
		# Cluster Result and its Original Data Value
		new_point2 = [cluster_final_header] + list_e_feature[cluster_index].split(',')
		# Cluster Result and the index of its Cluster Head
		new_data.append(new_point)
		new_data2.append(new_point2)
	#	print new_point
	#	print new_point2
	return new_data, new_data2

def DAP(d,numeric_list,nominal_list,Pinit):
	feature_ch = []
	feature_cluster = []
	q = s1(d,numeric_list,nominal_list,Pinit)
	# q is a list of Similarity Matrix for each unique value in each Feature
	for i in range(len(q)):
		ch,c = ap_rawdata(q[i])
		# ch is a list of cluster head for Feature(i)
		# c is a list of clustering result for each unique value in Feature(i)
		c = [ch[i] for i in c]
		# it seems to be replace each unique value in Feature(i) as its cluster head
		feature_ch.append(list(ch))
		feature_cluster.append(list(c))
		# feature_ch is a list of cluster head in each Feature
		# feature_cluster is a list of ClusterHead for each unique value in each Feature
	print "s3"
	S,new_d = s3(d,feature_cluster,numeric_list,nominal_list,Pinit)
	# new_d is the dataset with unique combination of values, where i-th value in a combination is the index of the cluster head of that value in feature(i)
	# S is the similarity matrix of new_d
	data_ch, data_cluster = ap_rawdata(S)
	# data_ch is a list of cluster head for new_d
	# data_cluster is a list of clustering result for each data in new_d
	data_ch = list(data_ch)	
	data_cluster = list(data_cluster)	
	print "q = ",q
	print "feature_ch = ", feature_ch
	print "feature_cluster = ",feature_cluster
	#print "data_cluster = ",data_cluster
	#print "data_ch = ",data_ch

	d1,d2 = s4(d,feature_cluster,data_cluster,numeric_list,nominal_list)
	#print d2
	#print len(S)
	return d1,d2,data_ch,data_cluster,S

#	modified in 2015.11.17
#	Calculate_Simi_Matrix means calculating the parameters of Simi Matrix in the combinations based on given each feature's simi matrix

def Calculate_Simi_Matrix(d1,d2,S):
	result = 0.0
	if d1[len(d1)-1]==',':
		d1 = d1[:-1]
	if d2[len(d2)-1]==',':
		d2 = d2[:-1]
	d1 = d1.split(",")
	d2 = d2.split(",")
	if len(d1)!=len(d2):
		print "the length of two data is different ....... "
	for i in range(len(d1)):
		data1 = int(d1[i])
		data2 = int(d2[i])
	#	print "data1,data2 = ",data1," ",data2
		try:
			result = result + S[i][data1][data2]
		except:
		#	print "data1,data2 = ",data1," ",data2," ",i
		#	print S[i]
		#	print len(S)
		#	print len(S[i])
			pass
	return result

#	modified in 2015.11.17
#	DAP_CR means DAP aims at Cluster Result
#	in DAP_CR, the program will deal with the data made by Cluster Result in different layers
#	In DAP_CR, d[i][j] means i-th data in j-th feature (plz notice this definition!)

def DAP_CR(d,S,numeric_list,nominal_list,Pinit):

#	find the unique combination and count their apperance times
#	extrected_feature = zip(*d)
#	extrected_feature_string = [str(ex_index).replace('(','').replace(')','').replace('\'','').replace(' ','') for ex_index in extrected_feature]

	extrected_feature_string = []
	for i in range(len(d)):
		tmp = ''
		for j in range(len(d[i])):
			tmp = tmp + str(d[i][j]) + ','
		extrected_feature_string.append(tmp)
	count_e_feature = Counter(extrected_feature_string)
	list_e_feature = list(count_e_feature)

#	print "list_e_feature = ",list_e_feature

#	calculate the similarity matrix between two unique combinations
	self_preference = []
	Simi = []
	for i in range(len(list_e_feature)):
		Simi_line = []
		for j in range(len(list_e_feature)):
			Simi_result = 0
			# Simi_result means Simi[i][j]
			if i==j:
				Simi_result = 0.0
				# Simi[i][i] will be modified later
				pass
			if i!=j:
				Simi_result = Calculate_Simi_Matrix(list_e_feature[i],list_e_feature[j],S)
				pass
			if i>j:
				self_preference.append(Simi_result)
			Simi_line.append(Simi_result)
		Simi.append(Simi_line)

	if Pinit == 0:
		preference_median = median(self_preference)
	else:
		preference_median = min(self_preference)
	n_max = count_e_feature.most_common()[0][1]
	print "n_max = ",n_max
	for i in range(len(list_e_feature)):
		Simi[i][i] = preference_median * (float(n_max)-float(count_e_feature[list_e_feature [i]]) + 1.0) / (float(n_max)+1.0)

#	put the new similarity matrix Simi[i][j] into ap_rawdata
#	and get every unique combination's cluster result

	print "ap_rawdata"

	data_ch,data_cluster = ap_rawdata(Simi)

#replace the unique combination's cluster result

	d1 = []
	d2 = []
	for i in range(len(d)):
		tmp = ""
		for j in range(len(d[i])):
			tmp = tmp+str(d[i][j])+','
	#	print tmp
	#	print list_e_feature
		for q in range(len(list_e_feature)):
			if list_e_feature[q]==tmp:
				cluster_index = q
				break
	#	print "cluster_index = ",cluster_index
	#	print data_cluster
	#	print data_ch
		cluster_label = -1
		cluster_label = data_cluster[cluster_index]
		new_point1 = [cluster_label] + [d[i]]
		new_point2 = [cluster_label] + [list_e_feature[cluster_index]]
		d1.append(new_point1)
		d2.append(new_point2)
	#	while True:
	#		pass

	return d1,d2

def DAP_nq(d,numeric_list,nominal_list,Pinit):
	feature_ch = []
	feature_cluster = []
	q = s1(d,numeric_list,nominal_list,Pinit)
	#for i in range(len(q)):
	#	ch,c = ap_rawdata(q[i])
	#	c = [ch[i] for i in c]
	#	feature_ch.append(list(ch))
	#	feature_cluster.append(list(c))
	for i in range(len(q)):
		feature_cluster.append(range(len(q[i])))
#	print feature_cluster
	S,new_d = s3(d,feature_cluster,numeric_list,nominal_list,Pinit)
	data_ch, data_cluster = ap_rawdata(S)
	data_ch = list(data_ch)
	data_cluster = list(data_cluster)
	d1,d2 = s4(d,feature_cluster,data_cluster,numeric_list,nominal_list)
	return d1,d2


def Evaluation():
	a = 1
	return a
