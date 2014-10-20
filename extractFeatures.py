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

	feature = extractFeatureVector(req)
	print feature





