from mylib import *
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import math

sessionDurationThreshold = 30	#in minutes;
# i.e. if the diff between prev request and next request is > threshold then,  it's a new session.


files = sys.argv[1]
saveflag = int(sys.argv[2])


print files
fname = files

lines = readFile(fname)
userMap={}
prevtime = 0
for line in lines:
	arr = getArray(line)
	username = str(getEmailAddr(arr))
	if getStatusCode(arr) != 200 or username == "-" or getReqSize(arr)==0:
		continue
	reqType = getReqType(arr)
	timeArr = getTime(arr)
	if not userMap.has_key(username):
		userMap[username]=[[],[],[],[],[]]

	timeInMin = timeInMinutes(timeArr)
	timeInSec = timeInSeconds(timeArr)
	reqObjType = getReqObjType(arr)
	if timeInMin < prevtime:
		timeInMin += 24*60	# for cases like when 23:59 and then 00:02. So add 24*60.
		timeInSec += 24*60*60
	prevtime = timeInMin
	userMap[username][0].append(timeInMin)	#Time In Minutes
	userMap[username][1].append(getReqSize(arr))	#Request Size
	userMap[username][2].append(reqType)	#GET or POST
	userMap[username][3].append(timeInSec)	#Needed for interarrival times 
	userMap[username][4].append(reqObjType)	#video,image,html etc



# for a particular user, given start index and end index of the session.
# It filters out the get and post requests. 
# The returned timeline is in seconds
def separateGetandPost(user, start, end):
	timelineGET=[]
	timelinePOST=[]
	reqGET = []
	reqPOST = []
	for i in range(start,end):
		if userMap[user][2][i] == "GET":
			timelineGET.append(userMap[user][3][i])
			reqGET.append(userMap[user][1][i])
		else:
			timelinePOST.append(userMap[user][3][i])
			reqPOST.append(userMap[user][1][i])
	return timelineGET, reqGET, timelinePOST, reqPOST

# returns the timeline of videos and their sizes
# Again timeline returned is in seconds
def separateVideos(user, start, end):
	timelineVideo=[]
	reqVideo = []
	for i in range(start,end):
		if userMap[user][4][i] == "video":
			timelineVideo.append(userMap[user][3][i])
			reqVideo.append(userMap[user][1][i])
	return timelineVideo, reqVideo

# returns the array containing start indices of the sessions
def identifySession(timeline): #timeline is array of time(in minutes)
	sessionStartIndex = [0] #first session starts at index=0
	prev = timeline[0]
	for i in range(len(timeline)):
		time = timeline[i]
		if (time-prev) > sessionDurationThreshold:
			sessionStartIndex.append(i)
		prev = time
	return sessionStartIndex

# returns list of session-durations given timeline(in minutes) and session-startindex-markers
def sessionDuration(timeline):
	sessionStartIndex = identifySession(timeline)
	duration = []
	for i in range(len(sessionStartIndex)):
		index = sessionStartIndex[i]
		# print index
		if i == len(sessionStartIndex)-1:
			endIndex = len(timeline) - 1
		else:
			endIndex = sessionStartIndex[i+1] - 1
		duration.append(timeline[endIndex] - timeline[index])
	return duration

# return a list of session-counts per user, 
# to give a high level overview of the sessions per user per day
def sessionCountList():
	sessionCountList = []
	for user in userMap.keys():
		timeline = userMap[user][0]
		if not timeline:
			print user+" : with timeliine empty"
		else:
			sessionCountList.append(len(identifySession(timeline)))
	return sessionCountList


# Input: the timeline of a session
def interArrivalTime(timeline):
	return [timeline[i]-timeline[i-1] for i in range(1,len(timeline))]

# Can plot all the sessions of the user, separating get and post requests

def plotSession(user):

	sessionStartIndex = identifySession(userMap[user][0])
	for i in range(len(sessionStartIndex)):
		index = sessionStartIndex[i]
		# print index
		if i == len(sessionStartIndex)-1:
			endIndex = len(userMap[user][0])
		else:
			endIndex = sessionStartIndex[i+1]

		timelineGET, reqGET, timelinePOST, reqPOST = separateGetandPost(user, index, endIndex)
		# timelineVideo, reqVideo = separateVideos(user, index, endIndex)

		startTime = 0
		if not timelineGET:
			startTime = timelinePOST[0]
		elif not timelinePOST:
			startTime = timelineGET[0]
		else:
			startTime = min(timelineGET[0], timelinePOST[0])
		
		timelineGET = [time - startTime for time in timelineGET]
		# timelineVideo = [float(time - startTime)/60 for time in timelineVideo]
		# interAT = interArrivalTime(timelineVideo)
		# if not interAT:
		# 	continue
		# plotHistogram1(interAT,False,range(0,100,5),False,False,0,user+", session="+str(i+1),"InterArrival Distribution",1 )
		# overallInterArrivalTimes.append(giveStats(interAT)["mean"])
		# if(len(timelineVideo)>50):
			# continue
		# overallVideosPerSession.append(len(timelineVideo))


		timelinePOST = [time - startTime for time in timelinePOST]
		reqGET = map(math.log, reqGET)
		reqPOST = map(math.log, reqPOST)
		plt.plot(timelineGET, reqGET, marker='o')
		plt.plot(timelinePOST, reqPOST, marker='o')
		plt.show()

def interArrivals():	
	overallInterArrivalTimes = []
	overallInterArrivalTimesVideos = []
	overallVideosPerSession = []
	c=0
	for user in userMap.keys():
		sessionStartIndex = identifySession(userMap[user][0])
		for i in range(len(sessionStartIndex)):
			index = sessionStartIndex[i]
			# print index
			if i == len(sessionStartIndex)-1:
				endIndex = len(userMap[user][0])
			else:
				endIndex = sessionStartIndex[i+1]

			# Get Requests
			timelineGET, reqGET, timelinePOST, reqPOST = separateGetandPost(user, index, endIndex)
			startTime = 0
			if not timelineGET:
				startTime = timelinePOST[0]
			elif not timelinePOST:
				startTime = timelineGET[0]
			else:
				startTime = min(timelineGET[0], timelinePOST[0])
			
			timelineGET = [time - startTime for time in timelineGET]
			interAT = interArrivalTime(timelineGET)
			if interAT:
				overallInterArrivalTimes.append(giveStats(interAT)["mean"])
			else:
				c+=1

			# Videos
			timelineVideo, reqVideo = separateVideos(user, index, endIndex)
			overallVideosPerSession.append(len(timelineVideo))

			if not timelineVideo:
				continue
			else:
				startTime = timelineVideo[0]
				timelineVideo = [float(time - startTime)/60 for time in timelineVideo]
				interAT = interArrivalTime(timelineVideo)
				
				if interAT:
					overallInterArrivalTimesVideos.append(giveStats(interAT)["mean"])

				if(len(timelineVideo)>50):
					continue

	return overallInterArrivalTimes, overallInterArrivalTimesVideos, overallVideosPerSession

# Plots the histogram of the session duration
def plotSessionDuration():
	durationList = []
	for user in userMap.keys():
		timeline = userMap[user][0]
		durationList += sessionDuration(timeline)
	plotHistogram(durationList,False,20,False,False,saveflag,"Session duration",
		fname+": Distribution of session duration\nAssuming threshold="+str(sessionDurationThreshold)+" minutes",1)


# plotSessionDuration()
# sessionCountList = sessionCountList()
# plotHistogram(sessionCountList,False,10,False,False,1,"Number of User-sessions per day","Session Count distribution",1)

# print sampleUser
# for sampleUser in userMap.keys():
# 	plotSession(sampleUser)
	
# overallInterArrivalTimes = [float(ele)/60 for ele in overallInterArrivalTimes] #Done for video objects
# plotHistogram1(overallInterArrivalTimes,False,range(0,30,1),
	# False,False,0,"Overall Average InterArrival Time for Videos per session(in Min)","Overall Average InterArrival Time for Videos per session",1)

# plotHistogram1(overallVideosPerSession,False,range(0,50,1),
# 	False,False,0,"Number of videos per session","Distribution of Number of videos per session",1)

'''
# def plotHistogram(l, cumulative_flag=True,nbins=10, both=False, isNormed=False,saveflag=0 ,xlabel="xlabel", title="Title", legendLoc=4):
'''
plotSessionDuration()
sessionCountList = sessionCountList()
plotHistogram(sessionCountList,False,10,False,False,saveflag,"Number of User-sessions per day",fname+": Session Count distribution",1)

overallInterArrivalTimes, overallInterArrivalTimesVideos, overallVideosPerSession = interArrivals()

plotHistogram1(overallInterArrivalTimes,False,range(0,100,2),
	False,False,saveflag,"Overall Average InterArrival Time per session(in seconds)",fname+": Overall Average InterArrival Time per session",1)


plotHistogram1(overallInterArrivalTimesVideos,False,range(0,30,1),
	False,False,saveflag,"Overall Average InterArrival Time for Videos per session(in Min)",fname+": Overall Average InterArrival Time for Videos per session",1)

plotHistogram1(overallVideosPerSession,False,range(0,50,1),
	False,False,saveflag,"Number of videos per session","Distribution of Number of videos per session",1)

