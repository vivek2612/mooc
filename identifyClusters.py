from mylib import *
import os
import sys
import math
from Cluster import *
from globalmaps import *

matrix_dir = "matrix_dir" # dir containing the files corresponding to users' session matrices.
allFiles = os.listdir(matrix_dir)



# Take first K files. From each file, pick up the first matrix or point as the centroid.
# This is done to initialze clusters. 
def initClusters():
	i = 0;
	clusterList = []
	for afile in allFiles:
		if(i==K):
			break
		f = open(matrix_dir+"/"+afile,'r')
		lines = f.readlines()
		f.close()
		for line in lines:
			centroid = eval(line)
			cluster = Cluster(centroid);
			clusterList.append(cluster)
			break
		i += 1
	return clusterList
	
allPoints = []	#Each point represent one matrix
# Read all the files. Pick up all the points/matrices from the file and dump ...
# it in allPoints array
def collectAllPoints():
	for afile in allFiles:
		f = open(matrix_dir+"/"+afile,'r')
		lines = f.readlines()
		f.close()
		for line in lines:
			mat = eval(line)
			allPoints.append(mat)

# Runs K-means clustering algorithm for nIterations times.
def runClustering(nIterations):
	while (nIterations!=0):
		for cluster in clusterList:
			cluster.nMembers = 0
		for point in allPoints:
			dist = []
			for cluster in clusterList:
				dist.append(cluster.getDistance(point))
			minDist = min(dist)
			clusterIndex = dist.index(minDist)
			clusterList[clusterIndex].updateCluster(point) #updates the centroid of the cluster
			# On last iteration, store each point with its cluster.
			# Will be used to find intra-cluster distance later.
			if(nIterations==1):
				clusterList[clusterIndex].addPointToCluster(point)
		nIterations -= 1


# After clustering is complete, Returns mean, variance, and ...
# coefficient of variation of intra-cluster distances. 
def intraClusterStats():
	summation = 0.0
	for cluster in clusterList:
		summation += cluster.intraClusterDist()
	mean = summation / float(K)
	summation = 0.0
	for cluster in clusterList:
		summation += (cluster.intraClusterDist() - mean)**2
	variance = summation / float(K-1)
	coeffVariation = math.sqrt(variance)/ mean
	return coeffVariation

# distance b/w two clusters = distance b/w their centroids
# Used in calculating inter cluster statistics
def getDistaceBwClusters(cluster1, cluster2):
	centroid1 = cluster1.centroid
	centroid2 = cluster2.centroid
	sumOfSquares = 0
	n = len(stateList)
	for i in range(n):
		for j in range(n):
			sumOfSquares += (centroid1[i][j] - centroid2[i][j]) ** 2 
	return math.sqrt(sumOfSquares)

# Dij : distance between two clusters. 
def interClusterStats():
	nDistances = float((K*(K-1))/2.0)
	distances  = []
	for i in range(K):
		for j in range(i+1, K):
			distances.append(getDistaceBwClusters(clusterList[i], clusterList[j]))
	mean = sum(distances) / nDistances
	summation = 0.0
	for dist in distances:
		summation += (dist - mean)**2 
	variance = summation / (nDistances-1)
	coeffVariation = math.sqrt(variance)/ mean
	return coeffVariation 



collectAllPoints()
nIterations = 10
clusterList = []# list of cluster obejects.
K = 4
clusterList = initClusters()
runClustering(nIterations)
for cluster in clusterList:
	print cluster.nMembers

coeffVariation_intra = intraClusterStats()
print coeffVariation_intra
coeffVariation_inter = interClusterStats()
print coeffVariation_inter



