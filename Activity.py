from globalMaps import *
class Activity:
	name = ""
	isComplete = False	#Whether all the required features have been seen for the activity
	featuresCount = 0

	def __init__(self,activityName):
		name = activityName
	
	def getFeatures(self):
		return activityFeaturesMap[name]

	def update(feature):
		featuresCount += 1
		if not name in uncountableActivities:
			if featuresCount == len(activityFeaturesMap[name]):
				isComplete = True

	def canAccomodate(feature):
		if name=="thread_clicking":
			if feature==['GET', 'json', 'comments'] and featuresCount!=0:
				return False
			else:
				return True
		else:
			return True

	def isFull():
		return isComplete


'''
Imported from globalMaps
# stateList=[]
# activityFeaturesMap={}
# featureActivityMap={}
# activityStateMap={}
'''