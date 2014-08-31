import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import re
plotDir = "plots"
#==============================================================================
# 							MACROS
#==============================================================================

endl = "\n"

#==============================================================================


def extractDate(date_elem):
	full_date = date_elem[1:] #date_elem = [24/Jun/2014:03:40:17
	date = "".join(full_date.split(":")[0].split("/"))
	return date #24Jun2014

def extractTime(date_elem):
	return [int(x) for x in  date_elem[1:].split(":")[1:]]


'''
The format of arr is given below : 

0 - ['vishalds735@gmail.com 1.187.161.5 - [24/Jun/2014:03:40:07 +0530]  ',
1 - 'GET /concept/3/null HTTP/1.1',
2 - ' 404 1164 ',
3 - 'http://14.139.97.83/concept/3/', 
4 - 'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0',
5 - ' 0.022 0.022 .\n']
'''
#==============================================================================

def getArray(line):
	arr = line.split('"')
	if(" " in arr):
		arr.remove(" ")
	return arr

def getEmailAddr(arr):
	return arr[0].strip().split(" ")[0]

def getIP(arr):
	return arr[0].strip().split(" ")[1]

def getDate(arr):
	date = arr[0].strip().split(" ")[-2].split(":")[0][1:]
	return date

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