
from globalmaps import *
class Session:
	C = [0]*len(stateList) #Count of visits matrix
	Z = [0]*len(stateList) #Stay time matrix
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
		f.close()

		# Writing waitTime matrix in a separate file. 
		waitTimefname = list(reversed(filename.split('/')))[0] #Input : "xdir/../.../log/user1" , output: 'user1'
		waitTimefname = waitTimefname.split("_")[0] #Input : username_matrix , output : username
		waitTimefname = "waitTimeMatrix_dir/" + waitTimefname
		f = open(waitTimefname, 'a');
		f.write(str(self.Z)+"\n");
		f.close()
		# print "written in file\n"

'''
Imported from globalMaps
# stateList=[]
# activityFeaturesMap={}
# featureActivityMap={}
# activityStateMap={}
'''