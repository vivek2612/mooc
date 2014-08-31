from mylib import *
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

'''
Take only videos in consideration, so take input as video file only.
why ? 
Ans : I found that, whole file => 626 entries
					vides file => 609 entries
					Not much difference
'''

files = sys.argv[1]
print files
fname = files

lines = readFile(fname)
histarr=[]
user_bandwidthMap={}
for line in lines:
	arr = getArray(line)
	ip = getIP(arr)
	req_size = getReqSize(arr)
	resp_time = getRespTime(arr)
	status_code = getStatusCode(arr)

	oneMB = 1024*1024
	if(req_size > oneMB and resp_time != 0 and status_code==200):
		bandwidth = (req_size/resp_time)/1024.0 #KBpS
		if ip in user_bandwidthMap.keys():
			user_bandwidthMap[ip].append(bandwidth)
		else:
			user_bandwidthMap[ip]=[bandwidth]


average_bandwidths=[]
for ip,bandwidths in user_bandwidthMap.items():
	average_bandwidths.append(sum(bandwidths)/len(bandwidths))



l=range(0,1000,50)
print printStats(average_bandwidths)
# plotHistogram(l, cumulative_flag=True,nbins=10, both=False, isNormed=False,saveflag=0 ,xlabel="xlabel", title="Title", legendLoc=4):

saveflag=int(sys.argv[2])
result = plotHistogram1(average_bandwidths, False, l, False, False,saveflag,"client bandwidth in KBPS", fname+" : bandwidth distribution",1 )



