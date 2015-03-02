# After the matrices have been generated. The clustering happens in this program. 

from mylib import *
import os
import sys
import math
from Cluster import *
from globalmaps import *

matrix_dir = "matrix_dir" # dir containing the files corresponding to users' session matrices.

allFiles = os.listdir(matrix_dir)
userClusterMap = {}  # {username : [1,1,0,0,4]} . i.e. count of sessions in each cluster


allPoints = []	#Each point represent one matrix
allWaitTimes = [] #Each point represent one wait-time matrix 
allUsernames = [] #All usernames corresponding to every matrix 
# Read all the files. Pick up all the points/matrices from the file and dump ...
# it in allPoints array
def collectAllPoints():
	for afile in allFiles:
		f = open(matrix_dir+"/"+afile,'r')
		lines = f.readlines()
		f.close()
		uname = afile.split("_")[0]
		userClusterMap[uname] = [0]*K
		for line in lines:
			mat = eval(line)	
			allPoints.append(mat)
			allUsernames.append(uname) #filename is same as username_matrix. 

		waitTimeMatrix_dir = "waitTimeMatrix_dir" 
		f = open(waitTimeMatrix_dir+"/"+uname,'r')
		lines = f.readlines()
		f.close()
		for line in lines:
			mat = eval(line)
			allWaitTimes.append(mat)


# Every 10th point is chosen as the cluster centroid. 
# This is done to initialze clusters. 
def initClusters():
	i = 0;
	clist = []
	for i in range(K):
		centroid = allPoints[i*10];
		centroid_waitTime = allWaitTimes[i*10]
		cluster = Cluster(centroid, centroid_waitTime);
		clist.append(cluster)
	return clist


# Runs K-means clustering algorithm for nIterations times.
def runClustering(nIterations):
	while (nIterations!=0):
		for cluster in clusterList:
			cluster.nMembers = 0
			cluster.memberList = []
			cluster.userList = []
		index = 0
		for point in allPoints:  #point here refers to the matrix. 
			dist = []
			for cluster in clusterList:
				dist.append(cluster.getDistance(point))
			minDist = min(dist)
			clusterIndex = dist.index(minDist)
			clusterList[clusterIndex].updateCluster(point, allWaitTimes[index]) #updates the centroid of the cluster
			# On last iteration, store each point with its cluster.
			# Will be used to find intra-cluster distance later.
			if(nIterations==1):
				uname = allUsernames[index]
				clusterList[clusterIndex].addPointToCluster(point, uname) #the username corresponding to the point
				userClusterMap[uname][clusterIndex] += 1

			index += 1
		nIterations -= 1



# After clustering is complete, Returns mean, variance, and ...
# coefficient of variation of intra-cluster distances. 
def intraClusterStats(clist):
	summation = 0.0
	for cluster in clist:
		summation += cluster.intraClusterDist()
	mean = summation / float(K)
	summation = 0.0
	for cluster in clist:
		summation += (cluster.intraClusterDist() - mean)**2
	variance = summation / float(K-1)
	coeffVariation = math.sqrt(variance)/ mean
	return variance, coeffVariation

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
def interClusterStats(clist):
	nDistances = float((K*(K-1))/2.0)
	distances  = []
	for i in range(K):
		for j in range(i+1, K):
			distances.append(getDistaceBwClusters(clist[i], clist[j]))
	mean = sum(distances) / nDistances
	summation = 0.0
	for dist in distances:
		summation += (dist - mean)**2 
	variance = summation / (nDistances-1)
	coeffVariation = math.sqrt(variance)/ mean
	return variance, coeffVariation 


nIterations = 10 #Though 5 were sufficient
K = int (sys.argv[1])
clusterList = []# list of cluster obejects.
collectAllPoints()
clusterList = initClusters()
runClustering(nIterations)
v_intra, coeffVariation_intra = intraClusterStats(clusterList)
v_inter, coeffVariation_inter = interClusterStats(clusterList)
# print K, v_intra, v_inter, coeffVariation_intra, coeffVariation_inter


# Now that you have the count of session in each cluster for a particular user, we need to decide 
# which cluster user belongs to. So we adopt approach of MAXFREQUENCY. 
# for uname in userClusterMap.keys():
# 	userClusterMap[uname] = userClusterMap[uname].index(max(userClusterMap[uname]))
# print userClusterMap

for user in userClusterMap.keys():
	print user, ":", userClusterMap[user]

for cluster in clusterList:
	cluster.normalize()
	# print cluster.centroid
	# print cluster.centroid_waitTime
	# print cluster.nMembers
	# print cluster.userList
	# print "=================================="





