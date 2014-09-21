statesfile='states.txt'
activityFeaturesMapfile='activity-features-mapping.txt'
featureActivityMapfile='feature-activity-mapping.txt'
activityStateMapfile='activity-state-mapping.txt'

stateList=[]
activityFeaturesMap={}
featureActivityMap={}
activityStateMap={}

uncountableActivities=["course_page_arrival", "contents_clicking", "thread_clicking"]

def initializeStates():
	f=open(statesfile, 'r')
	lines=f.readlines()
	for line in lines:
		stateList.append(line.strip())

def initializeActivityFeaturesMap():
	f=open(activityFeaturesMapfile, 'r')
	lines=f.readlines()
	for line in lines:
		arr = line.split(':')
		activityFeaturesMap[arr[0].strip()] = eval(arr[1].strip())

def initializeFeatureActivityMap():
	f=open(featureActivityMapfile, 'r')
	lines=f.readlines()
	for line in lines:
		arr = line.split(':')
		if str(eval(arr[0].strip())) in featureActivityMap.keys():
			print "Repeating: "+arr[0]
		featureActivityMap[str(eval(arr[0].strip()))] = arr[1].strip()

def initializeActivityStateMap():
	f=open(activityStateMapfile, 'r')
	lines=f.readlines()
	for line in lines:
		arr = line.split(':')
		activityStateMap[arr[0].strip()] = arr[1].strip()

def initializeAll():
	initializeStates()
	initializeActivityFeaturesMap()
	initializeFeatureActivityMap()
	initializeActivityStateMap()

initializeAll()


