
from globalMaps import *
class Session:
	C = [0]*len(stateList) #Count of visits matrix
	Z = [0]*len(stateList) #Think time matrix
	curState = None
	curActivity = None
	def __init__(self):
		for i in range(len(stateList)):
			C[i] = [0]*len(stateList)
			Z[i] = [0]*len(stateList)

	# def writeInFile(self):

'''
Imported from globalMaps
# stateList=[]
# activityFeaturesMap={}
# featureActivityMap={}
# activityStateMap={}
'''