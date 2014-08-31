import sys
import os
from mylib import *

files = sys.argv[1]
saveflag = int(sys.argv[2])

print files
# Need a video-requests file for it. 
fname = files

lines = readFile(fname)
'''
GET /media/static/video/transport-review.mp4 HTTP/1.1
'''
videoPopularityMap={}


histArr=[]
for line in lines:
	arr = getArray(line)
	status_code = getStatusCode(arr)
	if(status_code==200):
		request = getCompleteRequest(arr)
		reqObject = request.split()[1].strip()
		videoName = reqObject.split('/')[-1]
		histArr.append(videoName)
		if videoName in videoPopularityMap.keys():
			videoPopularityMap[videoName] += 1
		else:
			videoPopularityMap[videoName] = 1


fractionPerVideo = [float(count)*100/float(sum(videoPopularityMap.values())) for count in videoPopularityMap.values() ]

xticks =  videoPopularityMap.keys()
xvals =  range(0,len(videoPopularityMap.keys()))

plt.xticks(xvals, xticks)
plt.plot(xvals, fractionPerVideo, marker='o')
plt.plot(xvals, fractionPerVideo)
locs, labels = plt.xticks()
plt.setp(labels, rotation=90)

plt.grid()

plt.xlabel("Video Name")
plt.ylabel("Fraction of requests ")
plt.title(fname+" : Video popularity")

if(saveflag):
	plt.savefig(plotDir+"/"+title+".png")
else:
	plt.show()

# plt.savefig('plots/videoPopularity.png')

