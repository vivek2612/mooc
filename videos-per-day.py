import sys
import os
from mylib import *

files = sys.argv[1]
print files
# Need a video-requests file for it. 
fname = files

lines = readFile(fname)
'''
GET /media/static/video/transport-review.mp4 HTTP/1.1
'''
videosPerDayPerUser={}
for line in lines:
	arr = getArray(line)
	status_code = getStatusCode(arr)
	if(status_code==200):
		username = getEmailAddr(arr)
		request = getCompleteRequest(arr)
		reqObject = request.split()[1].strip()
		videoName = reqObject.split('/')[-1]

		if(username in videosPerDayPerUser.keys()):
			if not videoName in videosPerDayPerUser[username]:
				videosPerDayPerUser[username].append(videoName)
		else:
			videosPerDayPerUser[username] = [videoName]


videosCount = [len(value) for value in videosPerDayPerUser.values() ]


# plotHistogram(l, cumulative_flag=True,nbins=10, both=False, isNormed=False,saveflag=0 ,xlabel="xlabel", title="Title", legendLoc=4):plotHistogram(videosCount,False, 58, True, 0,"Videos Per day Per user", "Distribution of videos per day", 4)
saveflag = int(sys.argv[2])
plotHistogram(videosCount,False, 60, False, True,0,"Videos Per day Per user", fname+ ": Distribution of videos per day", 1)
