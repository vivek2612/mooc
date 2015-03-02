statesfile='states.txt'
activityFeaturesMapfile='activity-features-mapping.txt'
featureActivityMapfile='feature-activity-mapping.txt'
activityStateMapfile='activity-state-mapping.txt'

stateList={} #{state : stateID}
activityFeaturesMap={} #{activity : feature}
featureActivityMap={}	#{feature : activity_name}
activityStateMap={}	#{activity_name : stateName}

uncountableActivities=["course_page_arrival", "contents_clicking", "thread_clicking",\
						"courses_clicking", "bodhitree_clicking", "login_clicking", "my_courses_clicking"]

ignoredFeatures = [['GET', 'html', 'media'],['GET', 'ico']]

#uncountableActivities : the activities which donot have a fixed number of features. 
# For eg. : "thread_clicking" can induce many requests for replies of that thread.
# The bottom 4 "courses_clicking", "bodhitree_clicking", "login_clicking", "my_courses_clicking" 
# 	are due to presence of course_image. (Since there can be multiple courses. )

def initializeStates():
	f=open(statesfile, 'r')
	lines=f.readlines()
	count = 0
	for line in lines:
		stateList[line.strip()] = count
		count += 1

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


