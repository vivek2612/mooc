

'''
The format of arr is given below : 

0 - ['vishalds735@gmail.com 1.187.161.5 - [24/Jun/2014:03:40:07 +0530]  ',
1 - 'GET /concept/3/null HTTP/1.1',
2 - ' 404 1164 ',
3 - 'http://14.139.97.83/concept/3/', 
4 - 'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0',
5 - ' 0.022 0.022 .\n']
'''

from mylib import *
import os
import sys
import matplotlib.pyplot as plt
import numpy as np


files = sys.argv[1]
saveflag=int(sys.argv[2])
print files, saveflag
fname = files

requestMap={}

def initializeRequestMap():
	requestMap["js"]=[0,0]
	requestMap["html"]=[0,0]
	requestMap["css"]=[0,0]
	requestMap["font"]=[0,0]
	requestMap["image"]=[0,0]
	requestMap["video"]=[0,0]
	requestMap["json"]=[0,0]

initializeRequestMap()


lines = readFile(fname)
for line in lines:
	arr = getArray(line)
	status_code = getStatusCode(arr)
	reqSize = getReqSize(arr)
	if(not isValidStatusCode(status_code) or reqSize==0):
		continue

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
	requestMap[rtype][0] += 1
	requestMap[rtype][1] += reqSize/1024


labels = requestMap.keys()
fracs = [value[0] for value in requestMap.values()]
title = 'Fraction of each type of request'  
drawPieChart(labels,fracs,title,saveflag)

#traffic
fracs = [value[1] for value in requestMap.values()]
title = 'Fraction of traffic of each type of requests'

drawPieChart(labels,fracs,title,saveflag)

