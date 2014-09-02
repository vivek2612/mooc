import sys
import os
from mylib import *

fname = sys.argv[1]
print fname
# Need a video-requests file for it. 

lines = readFile(fname)
createIpUserMap(lines)

videosPerDayPerUser={}
for line in lines:
	arr = getArray(line)
	status_code = getStatusCode(arr)
	if isValidStatusCode(status_code):
		username = getUsername(arr)
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
