from mylib import *
import os
import sys



fname = sys.argv[1]

lines = readFile(fname)

'''
GET /forum/api/comment/39/replies/?format=json HTTP/1.1
'''
for line in lines:
	arr = getArray(line)
	req = getCompleteRequest(arr)
	# arr = line.split()

	arr = req.split()
	reqType = arr[0].strip()
	reqArr = list(reversed(arr[1].split('/')))
	feature = []

	feature.append(reqType) #GET or POST
	i = 0	
	if reqArr[i].strip()=="" or is_number(reqArr[i].strip()):
		feature.append('html')
	else:
		if '.' in reqArr[i]:
			reqArr[i] = reqArr[i].split('.')[1]
		params = reqArr[i].strip('? ').split('&')
		for ele in params:
			ele = ele.split('=')
			if ele[0]!="format":
				feature += [ele[0]]
			else:
				feature += [ele[1]]

		
	if(reqArr[i+1]==""):
		feature.append('HOME')
	elif is_number(reqArr[i+1].strip()):
		feature.append(reqArr[i+2])
	else:
		feature.append(reqArr[i+1])
	print feature





