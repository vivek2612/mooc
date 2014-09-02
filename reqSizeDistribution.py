from mylib import *
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

files = sys.argv[1]
reqType = sys.argv[2]
saveflag=int(sys.argv[3])

print files
fname = files
lines = readFile(fname)
reqSizeArr=[]
user_bandwidthMap={}
for line in lines:
	arr = getArray(line)
	if not isValidStatusCode(getStatusCode(arr)):
		continue
	req_size = getReqSize(arr)
	if reqType=="video":
		req_size = req_size/(1024.0*1024.0)
	reqSizeArr.append(req_size)
	

# l=[0,100,200,300,400,500,600,700,800,900,1000,1500,2000,3000,4000,5000,10000,20000,30000,40000]
l=[]
if reqType=="video":
	l =	range(0,50,1)#MB
else:
	l = range(0,10000,100)
print printStats(reqSizeArr)
# def plotHistogram(l, cumulative_flag=True,nbins=10, saveflag=0 ,xlabel="xlabel", title="Title", legendLoc=4):

xlabel = reqType+" : Req-size"
title = ": CDF of Distribution of size of Requests"
legendLoc = 4
# plotHistogram(l, cumulative_flag=True,nbins=10, both=False, isNormed=False,saveflag=0 ,xlabel="xlabel", title="Title", legendLoc=4):

if reqType=="video":
	result = plotHistogram1(reqSizeArr, True, tuple(l), False, False, saveflag, xlabel+"(in MB)", fname+title, legendLoc)
else:
	result = plotHistogram(reqSizeArr, True, 200, False, False, saveflag, xlabel+"(in bytes)", fname+title, legendLoc)




