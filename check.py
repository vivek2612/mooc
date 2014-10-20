from mylib import *
import os
import sys
import math
from Activity import *
from Session import *

threshold = 30 # 30 minutes threshold
fname = sys.argv[1] # file with logs of only single user
lines = readFile(fname)


prevtime = -1
curSession = Session()
sessionInProgress = False

for line in lines:
	arr = getArray(line)
	req = getCompleteRequest(arr)
	print req
	print extractFeatureVector(req)