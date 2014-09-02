import sys
import os
from mylib import *



def findBin(timeArr, binSizeInMin):
	t = timeInSeconds(timeArr)
	return t/(binSizeInMin*60)

def createTimeLine(binSize):
	timeLine = [ binSize*i for i in range(1,((24*60/binSize)+1)) ]
	for i in range(len(timeLine)):
		ele = timeLine[i]
		hour = ele/60
		minutes = ele%60
		timeLine[i] = str(hour)+":"+str(minutes)
	return timeLine

fname = sys.argv[1]
saveflag = int(sys.argv[2])


lines = readFile(fname)
binSize = 60 #user access pattern; time gap of binsize
countsPerBin = [0]*(24*60/binSize)
for line in lines:
	arr = getArray(line)
	if isValidStatusCode(getStatusCode(arr)):
		time = getTime(arr)
		countsPerBin[findBin(time,binSize)] += 1


fractionPerBin = [float(count)/float(sum(countsPerBin)) for count in countsPerBin ]
cumFractionPerBin = np.cumsum(fractionPerBin)

xticks =  createTimeLine(binSize)
xvals = [ binSize*i for i in range(1,((24*60/binSize)+1)) ]

fig, ax1 = plt.subplots()

plt.xticks(xvals, xticks)
ax1.plot(xvals, fractionPerBin, marker='o')
ax1.plot(xvals, fractionPerBin)
locs, labels = plt.xticks()
plt.setp(labels, rotation=90)


ax2 = ax1.twinx()
ax2.plot(xvals, cumFractionPerBin, color='r')

ax1.grid()
ax2.grid()

title = fname + " : User Access Pattern"
plt.title(title)
plt.xlabel("Timeline")
ax1.set_ylabel("fraction of viewership")
ax2.set_ylabel("Cumulative fraction of viewership")

if(saveflag):
	plt.savefig(plotDir+"/user-access-pattern"+".png")
else:
	plt.show()
