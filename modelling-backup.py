from mylib import *
import os
import sys
import math
from Activity import *
from Session import *

threshold = 30 # 30 minutes threshold
fname = sys.argv[1] # file with logs of only single user
lines = readFile(fname)

matrix_fname = list(reversed(fname.split('/')))[0] #Input : "xdir/../.../log/user1" , output: 'user1'
matrix_fname += "_matrix" #user1_matrix
matrix_dir = "matrix_dir"
createDir(matrix_dir) #createDir creates (if not exists) matrix_dir in current directory.
matrix_fname = matrix_dir+"/"+matrix_fname
f = open(matrix_fname,'w')
f.close()


prevtime = -1
curSession = Session()
# print "New Session..."

for line in lines:
	arr = getArray(line)
	timeArr = getTime(arr)
	statusCode = getStatusCode(arr)

	timeInMin = timeInMinutes(timeArr)
	if timeInMin < prevtime:
		timeInMin += 24*60	# for cases like when 23:59 and then 00:02. So add 24*60.
	
	if ((timeInMin - prevtime) > threshold) and prevtime != -1:
		# print "Closing old session"
		curSession.C[stateList[curSession.curState] ][stateList["exit"]] += 1
		curSession.writeInFile(matrix_fname)
		curSession = Session()
		
	elif curSession.curActivity and curSession.curActivity.name == "logout_clicking":
		# print "Closing old session"
		curSession.writeInFile(matrix_fname)
		curSession = Session()
		# print "New Session..."




	prevtime = timeInMin
	if(isRedirectionStatusCode(statusCode)): 
		continue

	request = getCompleteRequest(arr)
	if(request=="-"): continue
 	reqObject = request.split()[1].strip()



 	if (not isStaticReq(request)) or \
 		(isVideoJsPngObject(reqObject) or isVideoObject(reqObject) or isPdfObject(reqObject)) :
 		
 		# print request
 		feature = extractFeatureVector(request) #extractFeatureVector function is in myLib
 		# print feature
 		if (not feature):
 			continue

 		if(feature in ignoredFeatures): #ignoredFeatures is in globalMaps.py
 			continue

 		if(curSession.curActivity and feature in activityFeaturesMap[curSession.curActivity.name]):
 			#current line is a potential candidate for lying in the same activity as previous
 			if (not curSession.curActivity.isFull()) and\
 			 curSession.curActivity.canAccomodate(feature):
 			 curSession.curActivity.update(feature) #No transition

 			else:
 				# Another instance of same activity, Self Loop 
 				stateID = stateList[curSession.curState]
 				curSession.C[stateID][stateID] += 1
 				curSession.curActivity = Activity(curSession.curActivity.name) #reset activity
 				# print "(Transition) : ", curSession.curState, "=> ", curSession.curState
 				# print curSession.curActivity.name+" started..*************"


 		else:
 			# Activity is not same as the previous activity
 			# State Transition will follow

 			if(not featureActivityMap.has_key(str(feature))):
 				print "-------------------------------------------------------"
 				print feature, request
 				print "Could not find match of this feature !"
 				print "-------------------------------------------------------"
 				
 				continue

 			newActivityName = featureActivityMap[str(feature)]
 			prevStateId = stateList[curSession.curState]
 			newState = activityStateMap[newActivityName]
 			# print "(Transition) : ", curSession.curState, "=> ", newState
 			newStateId = stateList[newState] #the state need not be different
 			curSession.curActivity = Activity(newActivityName) #Reset activity
 			curSession.curActivity.update(str(feature)) #update activity
 			curSession.curState = newState #Update state (Transition)
 			Session.C[prevStateId][newStateId] += 1 

 			# print curSession.curActivity.name+" started..*************"

 	








	










