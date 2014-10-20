import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import re
#==============================================================================
plotDir = "plots"
endl = "\n"
MONTH_MAP = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 
			'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
dummyUser = "dummyUser" # for IP 127.0.0.1
ipUserMap={}
#==============================================================================

#==============================================================================

'''
10.2.64.116 - 120050083  [23/Aug/2014:07:41:16 +0530] 
GET /quiz/api/quiz/431/?format=json HTTP/1.1
 200 137 
http://bodhitree1.cse.iitb.ac.in/concept/62/
Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0
 0.007 0.007 .
'''


def getArray(line):
	arr = line.split('"')
	if(" " in arr):
		arr.remove(" ")
	return arr

def getRawUsername(arr):
	return arr[0].strip().split(" ")[2]

def sortOrder(item):
	val = item[1]
	return (val[0]-2012)*365*24*3600 + val[1]*30*24*3600 + val[2]*24*3600 +  val[3]

def getUsername(arr):
	username = getRawUsername(arr)
	if username != '-':
		return username
	else:
		if len(ipUserMap)==0:
			print "Initialize ipUserMap first."
			exit(0)
		else:
			if ipUserMap.has_key(getIP(arr)):
				usernameTimeMap = ipUserMap[getIP(arr)]
				l = sorted(usernameTimeMap.iteritems(), key=sortOrder,reverse=True)
				timestamps = [timestamp for username,timestamp in l]
				mytimestamp = getDate(arr)+[timeInSeconds(getTime(arr))]
				username = l[usernameIndex(timestamps, mytimestamp)][0]
				return username
			else:
				return dummyUser 

def usernameIndex(timestampList, timestamp ):
	for index in range(len(timestampList)):
		ts = timestampList[index]
		if compareTime(ts, timestamp)>0:
			return index
	return -1

def getIP(arr):
	return arr[0].strip().split(" ")[0]

def getDate(arr):
	date = arr[0].strip().split(" ")[-2].split(":")[0][1:]
	date = date.split('/')
	date[1] = MONTH_MAP[date[1]]
	date = [int(x) for x in date]
	return list(reversed(date))	#[year, month, day]

def getTime(arr): 
	temp = arr[0].strip().split(":")
	hour = int(temp[1])
	minutes = int(temp[2])
	secs = int(temp[3].split()[0])
	return [hour, minutes, secs]

def getCompleteRequest(arr):
	return arr[1].strip()

def getReqType(arr):
	return arr[1].strip().split(" ")[0]

def getStatusCode(arr):
	return int(arr[2].strip().split(" ")[0])

def getReqSize(arr):
	return float(arr[2].strip().split(" ")[1])

def getHttpReferer(arr):
	return arr[3].strip()

def getBrowserInfo(arr):
	return arr[4].strip()

def getRespTime(arr):
	return float(arr[5].strip().split(" ")[0])

def getUpstreamRespTime(arr):
	return arr[5].strip().split(" ")[1]


#==============================================================================

def median(mylist):
    sorts = sorted(mylist)
    length = len(sorts)
    if not length % 2:
        return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
    return sorts[length / 2]

def printStats(l):
	if not l:
		return ""
	result = "No. of elements : "+str(len(l))+ endl
	result += "min : "+str(min(l))+ endl
	result += "max : "+str(max(l))+ endl
	result += "mean : "+str(float(sum(l))/len(l))+ endl
	result += "median : "+str(median(l))
	return result

def giveStats(l):
	stats = {}
	stats["nElems"] = len(l)
	stats["min"] = min(l)
	stats["max"] = max(l)
	stats["mean"] = float(sum(l))/len(l)
	stats["median"] = median(l)
	return stats

def plotHistogram(l, cumulative_flag=True,nbins=10, both=False, isNormed=False,saveflag=0 ,xlabel="xlabel", title="Title", legendLoc=4):
	if(both):
		result = plt.hist(l,bins=nbins,normed=isNormed,cumulative=True,label=printStats(l), histtype='step')#,bins=tuple(l))		
		result = plt.hist(l,bins=nbins,normed=isNormed,cumulative=False)#, histtype='step')#,bins=tuple(l))		
	else:
		result = plt.hist(l,bins=nbins,normed=isNormed,cumulative=cumulative_flag,label=printStats(l))#, histtype='step')#,bins=tuple(l))		

	plt.title(title)
	plt.xlabel(xlabel)
	plt.legend(loc=legendLoc)
	if(saveflag==0):
		plt.show()
	else:
		createDir(plotDir)
		plt.savefig(plotDir+"/"+ xlabel+'.png')
	plt.clf()
	return result

def plotHistogram1(l, cumulative_flag=True,nbins=10, both=False, isNormed=False,saveflag=0 ,xlabel="xlabel", title="Title", legendLoc=4):
	fig, ax = plt.subplots(1,1)
	if(both):
		result = ax.hist(l,bins=nbins,normed=isNormed,cumulative=True,label=printStats(l), histtype='step')#,bins=tuple(l))		
		result = ax.hist(l,bins=nbins,normed=isNormed,cumulative=False)#, histtype='step')#,bins=tuple(l))		
	else:
		result = ax.hist(l,bins=nbins,normed=isNormed,cumulative=cumulative_flag,label=printStats(l))#, histtype='step')#,bins=tuple(l))		

	ax.set_xticks(nbins)
	plt.title(title)
	plt.xlabel(xlabel)
	plt.legend(loc=legendLoc)
	if(saveflag==0):
		plt.xticks(rotation="vertical")
		plt.show()
	else:
		plotDir = "plots"
		createDir(plotDir)
		plt.savefig(plotDir+"/"+ xlabel+'.png')
	plt.clf()
	return result

def drawPieChart(labels, fracs,title="title",saveflag=0):
	plt.figure(1, figsize=(6,6))
	plt.pie(fracs,  labels=labels,autopct='%1.1f%%')
	plt.title(title)
	if(saveflag==0):
		plt.show()
	else:
		plotDir = "plots"
		createDir(plotDir)
		plt.savefig(plotDir+"/"+ title+'.png')
	plt.clf()
#==============================================================================

def readFile(filename):
	current_dir = os.getcwd()
	f = open(current_dir + "/" + filename,'r')
	lines = f.readlines()
	f.close()
	return lines


def createDir(dirName):
	current_dir = os.getcwd()
	new_dir = current_dir + "/"+dirName
	if not os.path.exists(new_dir):
		os.mkdir(new_dir)

#===================================================================================

def isStaticReq(req): # as obtained from req = getCompleteRequest(arr)
	if "static" in req.split('/'):
		return True
	else:
		return False

def isImageObject(reqObject):
	val = re.match("(.*\.png)|(.*\.jpg)|(.*\.jpeg)|(.*\.JPEG)|(.*\.ico)|(.*\.JPG)", reqObject)
	return False if val is None else True

def isCssObject(reqObject):
	val = re.match("(.*\.css)", reqObject)
	return False if val is None else True

def isJsObject(reqObject):
	val = re.match("(.*\.js)|(.*\.jsx)", reqObject)
	return False if val is None else True

def isVideoObject(reqObject):
	val = re.match("(.*\.mp4)|(.*\.flv)", reqObject)
	return False if val is None else True

def isPdfObject(reqObject):
	val = re.match("(.*\.pdf)", reqObject)
	return False if val is None else True

def isVideoJsPngObject(reqObject):	#for detecting whether play button is clicked.
	val = re.match("(.*video-js.png)", reqObject)
	return False if val is None else True


def isFontObject(reqObject):
	val = re.match("(.*\.mp4)|(.*\.flv)", reqObject)
	return False if val is None else True

def isJsonObject(reqObject):
	val = re.match("(.*format=json)", reqObject)
	return False if val is None else True

def getReqObjType(arr):
	request = getCompleteRequest(arr)
	reqObject = request.split()[1].strip()
	reqObjArr = reqObject.split('/')
	rtype=""
	if 'js' in reqObjArr or isJsObject(reqObject):
		rtype = "js"
	elif 'css' in reqObjArr or isCssObject(reqObject):
		rtype = "css"
	elif 'video' in reqObjArr or isVideoObject(reqObject):
		rtype = "video"
	elif 'img' in reqObjArr or  isImageObject(reqObject):
		rtype = "image"
	elif 'fonts' in  reqObjArr or 'font' in reqObjArr or isFontObject(reqObject):
		rtype = "font"
	elif isJsonObject(reqObject):
		rtype = "json"
	else:
		rtype = "html"
	return rtype

########################################## Time Related functions

'''
arr = getArray(line)
timeArr = getTime(arr)
'''
def timeInSeconds(timeArr):
	return timeArr[0]*3600 + timeArr[1]*60 + timeArr[2]

def timeDifferenceInSecs(timeArr1, timeArr2):
	t1 = timeInSeconds(timeArr1)
	t2 = timeInSeconds(timeArr2)
	return (t2-t1)

def timeInMinutes(timeArr):
	return timeArr[0]*60 + timeArr[1]	


def compareTime(timestamp1, timestamp2): 
	#timestamp=[year, month, day, timeInSeconds]
	for x,y in zip(timestamp1, timestamp2):
		if(x == y):
			continue
		else:
			return (x-y) #return positive if t1>t2, else negative
	return 0 #In case everything is equal

def createIpUserMap(lines):
	global ipUserMap
	'''
	ipUserMap
	{IP : {username:[year, month, day, timeInSeconds]} }
	Also, The date and time are corresponding to the first request by that user.
	'''
	for line in lines:
		arr = getArray(line)
		ip = getIP(arr)
		username = getRawUsername(arr)
		if ip == '127.0.0.1':
			username = dummyUser
		if username == '-':
			continue
		if ipUserMap.has_key(ip):
			if not ipUserMap[ip].has_key(username):
				ipUserMap[ip][username] = getDate(arr)+[timeInSeconds(getTime(arr))]
		else:
			ipUserMap[ip] = {username:getDate(arr)+[timeInSeconds(getTime(arr))]}
	return ipUserMap

# 2xx responses are considered valid 
def isValidStatusCode(statusCode):
	if statusCode/100==2:
		return True
	else:
		return False

def isRedirectionStatusCode(statusCode):
	if statusCode/100==3:
		return True
	else:
		return False



def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# ====================================================================

def extractFeatureVector(req): # as obtained from req = getCompleteRequest(arr)
	arr = req.split()
	reqType = arr[0].strip()
	reqArr = list(reversed(re.split('\?|/',arr[1]))) #splitting by '?' and '/' and reversing. 
	feature = []

	# print reqArr
	# print req
	feature.append(reqType) #GET or POST
	i = 0	
	firstElem = reqArr[i].strip()
	if reqArr[i].strip()=="" or is_number(reqArr[i].strip()):
		feature.append('html')
	else:
		if '.' in reqArr[i]:	#for cases like video.mp4 and slides.pdf
			reqArr[i] = reqArr[i].split('.')[1]	#replace them by .mp4 and .pdf only
			if(reqArr[i]=="pdf"):
				feature.append(reqArr[i]);
				return feature

		params = reqArr[i].strip('? ').split('&')
		for ele in params:
			ele = ele.split('=')
			if ele[0]!="format":
				feature += [ele[0]]
			else:
				feature += [ele[1]]
		
	reqArr = [x for x in reqArr if x != '']
	if firstElem=="":
		i=-1
	if(i==-1 and len(reqArr)==0):
		feature.append('HOME')
	elif (i+2)<len(reqArr) and is_number( reqArr[i+1].strip()):
		feature.append(reqArr[i+2])
	elif (i+1 < len(reqArr)):
		feature.append(reqArr[i+1])

	if 'null' in feature:
		feature = None
	return feature