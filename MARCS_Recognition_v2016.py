#	源文件是MARCS_Recognition.py
#	写完硕论初稿之后发现增加了多层novelty detection的部分
#	实在不想去改原来的MARCS_Recognition.py（其实是已经改不动了）
#	所以重写了Recognition


#----------------------------------------------
#	Read Feature
#	Description:	read feature information from external file
#	Hints:	Feature file's format
#	<No.>	<Feature Name>
#	<No.>	<Feature Name>
#	<No.>	<Feature Name>....
#----------------------------------------------

def read_feature(filename):
	FILE = open(filename,'rU')
	feature = FILE.read()
	feature = feature.split('\n')
	FILE.close()
	if (feature[feature.__len__()-1])=="":
		feature = feature[:-1]
	for i in range(feature.__len__()):
		feature[i] = feature[i].split("\t")
	return feature

#----------------------------------------------
#	Read Clustering
#	Description:	read clustering results from external file
#----------------------------------------------

def read_clustering(filename):
	FILE = open(filename,'rU')
	clustering = FILE.read()
	clustering = clustering.split("\n")
	if clustering[clustering.__len__()-1] == "":
		clustering = clustering[:-1]
	FILE.close()
	return clustering

def Initialization(filename):
	
	FILE = open(filename,'rU')
	rawdata = FILE.read()
	FILE.close()
	decoded = json.loads(rawdata)
	print "Initial_Instance_filename = ", decoded['Initial_Instance_filename']
	print "Initial_Clustering_filename = ", decoded['Initial_Clustering_filename']
	print "metric_filename = ", decoded['metric_filename']
	print "feature filename = ", decoded["feature_filename"]
	#metric 在 master thesis中用不太到

	print "sub context = ",decoded["sub"]

	Sub_Feature  =[]
	Sub_Clustering = []
	for i in range(len(decoded["sub"])):
		print "#",i," sub processing..."
		print decoded["sub"][i]
		print decoded["sub"][i]["feature_filename"]
		print decoded["sub"][i]["clustering_filename"]
		Sub_Feature_item = read_feature(decoded["sub"][i]["feature_filename"])
		Sub_Clustering_item = read_clustering(decoded["sub"][i]['clustering_filename'])
		Sub_Feature.append(Sub_Feature_item)
		Sub_Clustering.append(Sub_Clustering_item)

	Instance = read_dataset(decoded['Initial_Instance_filename'],'\t')
	Instance = Convert2FloatArray(Instance)
	Feature = read_feature(decoded['feature_filename'])

	#read the clustering result from initial instances
	Clustering = read_clustering(decoded['Initial_Clustering_filename'])

	#Clustering_Metric = read_dataset(decoded['metric_filename'],'\t')
	#Clustering_Metric = Convert2FloatArray(Clustering_Metric)
	#return decoded["log_filename"], decoded["WL_filename"], decoded["Semantic_filename"], Instance , Clustering, Clustering_Metric

	return decoded['log_filename'], decoded['WL_filename'], decoded['Semantic_filename'], Instance, Clustering, Feature, Sub_Clustering, Sub_Feature

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

def Nd_Classifier_BUILD(Instance, Feature, Sub_Clustering_item, Sub_Feature_item):
	pass
	ND_Classifier_sub = []
	one_class_ND()


def NoveltyDetection_BUILD(Instance, Clustering, Feature, Sub_Clustering, Sub_Feature):
	pass
	ND_Classifier = []
	for i in range(Sub_Feature.__len__()):
		ND_Classifier.append(ND_Classifier_BUILD(Instance, Clustering, Feature, Sub_Clustering[i], Sub_Feature))

#----------------------------------------------
#	Main
#----------------------------------------------

def main():

	log_filename, WL_filename, Semantic_filename, Instance, Clustering, Feature, Sub_Clustering, Sub_Feature = Initialization(sys.argv[1])
	ND_Classifier = NoveltyDetection_BUILD(Instance, Clustering, Feature, Sub_Clustering, Sub_Feature)
	
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


