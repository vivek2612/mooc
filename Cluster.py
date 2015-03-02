import math

class Cluster:
	nMembers = 0 #No. of points falling into this cluster
	centroid = None
	centroid_waitTime = None
	nRows = 0
	nCols = 0
	memberList = []
	userList = []
	
	def __init__(self, _centroid, _centroid_waitTime):
		self.centroid = _centroid #Initialize the centroid
		self.centroid_waitTime = _centroid_waitTime #Initialize the centroid
		self.nRows = len(_centroid)
		self.nCols = len(_centroid[0])
		self.nMembers = 0
		self.memberList = []
		userList = []

	def updateCluster(self, matrix, matrix_waitTime): # updates centroid and nMembers
		for i in range(self.nRows):
			for j in range(self.nCols):
				self.centroid[i][j] = (self.nMembers*(float)(self.centroid[i][j]) + (float)(matrix[i][j]))
				self.centroid[i][j] = self.centroid[i][j] / (float)(self.nMembers+1)

				self.centroid_waitTime[i][j] = (self.nMembers*(float)(self.centroid_waitTime[i][j]) + (float)(matrix_waitTime[i][j]))
				self.centroid_waitTime[i][j] = self.centroid_waitTime[i][j] / (float)(self.nMembers+1)

		self.nMembers += 1

	def addPointToCluster(self, mat, username):
		self.memberList.append(mat)
		self.userList.append(username)


	def getDistance(self, matrix):
		sumOfSquares = 0
		for i in range(self.nRows):
			for j in range(self.nCols):
				sumOfSquares += (self.centroid[i][j] - matrix[i][j]) ** 2 
		return math.sqrt(sumOfSquares)

	def printCentroid(self):
		for i in range(self.nRows):
			print self.centroid[i]

	def printCentroid_waitTime(self):
		for i in range(self.nRows):
			print self.centroid_waitTime[i]

	def intraClusterDist(self):
		sumDist = 0
		for mat in self.memberList:
			sumDist += self.getDistance(mat)
		if(self.nMembers!=0):
			return sumDist/(float)(self.nMembers)
		else:
			return -1

	#Converting count values into probability values
	def normalize(self):
		for i in range(self.nRows):
			rowSum = 0;
			for j in range(self.nCols):
				rowSum += self.centroid[i][j]
			if rowSum==0:
				continue
			for j in range(self.nCols):
				self.centroid[i][j] /= rowSum
				self.centroid[i][j] = float('%.2f' % self.centroid[i][j])
			








		
