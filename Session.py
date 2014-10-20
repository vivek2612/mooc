
from globalmaps import *
class Session:
	C = [0]*len(stateList) #Count of visits matrix
	Z = [0]*len(stateList) #Think time matrix
	curState = None
	curActivity = None
	def __init__(self):
		for i in range(len(stateList)):
			self.C[i] = [0]*len(stateList)
			self.Z[i] = [0]*len(stateList)
			self.curState = "entry"

	def writeInFile(self, filename): # Assumption : file named filename already exists
		# write(append) matrices in the file
		f = open(filename, 'a');
		f.write(str(self.C)+"\n");
		# print "written in file\n"

'''
Imported from globalMaps
# stateList=[]
# activityFeaturesMap={}
# featureActivityMap={}
# activityStateMap={}
'''