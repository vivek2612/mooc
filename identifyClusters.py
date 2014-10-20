from mylib import *
import os
import sys
import math
from Cluster import *
from globalmaps import *

matrix_dir = "matrix_dir" # dir containing the files corresponding to users' session matrices.


K = 3; # k-means clustering algorithm
clusterList = [] # list of cluster obejects.

def initClusters(K):
	for i in range(K):
		n = len(stateList)
		centroid = [0]*n;
		for j in range(n):
			centroid[j] = [0]*n

		cluster = Cluster(centroid);
		clusterList.append(cluster)


initClusters(K)
allFiles = os.listdir(matrix_dir)
for afile in allFiles:
	f = open(matrix_dir+"/"+afile,'r')
	lines = f.readlines()
	f.close()
	for line in lines:
		mat = eval(line)
		dist = []
		for cluster in clusterList:
			dist.append(cluster.getDistance(mat))
		minDist = min(dist)
		clusterIndex = dist.index(minDist)
		clusterList[clusterIndex].updateCluster(mat)


for cluster in clusterList:
	cluster.printCentroid()
	print endl






