from globalmaps import *
class Activity:
	name = ""
	isComplete = False	#Whether all the required features have been seen for the activity
	featuresCount = 0

	def __init__(self,activityName):
		self.name = activityName
	
	def getFeatures(self):
		return activityFeaturesMap[self.name]

	def update(self, feature):
		self.featuresCount += 1
		if not self.name in uncountableActivities: #uncountableActivities from globalMap.py
			if self.featuresCount == len(activityFeaturesMap[self.name]):
				self.isComplete = True

	def canAccomodate(self, feature):
		if self.name=="thread_clicking":
			# thread_clicking activity.
			# featureCount!=0 means you have already seen 'comments' request.
			# So if a new comment request comes, it's not the same activity.
			if feature==['GET', 'json', 'comments'] and self.featuresCount!=0:
				return False
			else:
				return True
		else:
			return True

	def isFull(self):
		return self.isComplete


'''
Imported from globalMaps
# stateList=[]
# activityFeaturesMap={}
# featureActivityMap={}
# activityStateMap={}
'''