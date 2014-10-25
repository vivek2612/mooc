import math

class Cluster:
	nMembers = 0 #No. of points falling into this cluster
	centroid = None
	nRows = 0
	nCols = 0
	memberList = []
	
	def __init__(self, _centroid):
		self.centroid = _centroid #Initialize the centroid
		self.nRows = len(_centroid)
		self.nCols = len(_centroid[0])

	def updateCluster(self, matrix): # updates centroid and nMembers
		for i in range(self.nRows):
			for j in range(self.nCols):
				self.centroid[i][j] = (self.nMembers*(float)(self.centroid[i][j]) + (float)(matrix[i][j]))
				self.centroid[i][j] = self.centroid[i][j] / (float)(self.nMembers+1)
		self.nMembers += 1

	def addPointToCluster(self, matrix):
		self.memberList.append(matrix)

	def getDistance(self, matrix):
		sumOfSquares = 0
		for i in range(self.nRows):
			for j in range(self.nCols):
				sumOfSquares += (self.centroid[i][j] - matrix[i][j]) ** 2 
		return math.sqrt(sumOfSquares)

	def printCentroid(self):
		for i in range(self.nRows):
			print self.centroid[i]

	def intraClusterDist(self):
		sumDist = 0
		for mat in self.memberList:
			sumDist += self.getDistance(mat)
		if(self.nMembers!=0):
			return sumDist/(float)(self.nMembers)
		else:
			return -1







		
