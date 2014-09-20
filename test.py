from mylib import *
import os
import sys
import matplotlib.pyplot as plt
import numpy as np



fname = sys.argv[1]

lines = readFile(fname)

outfile = open(fname+'-simplified','w')
for line in lines:
	arr = getArray(line)
	req = getCompleteRequest(arr)
	ref = getHttpReferer(arr);
	statusCode = getStatusCode(arr);
	outfile.write(str(statusCode)+", "+req+", "+ ref+'\n')

outfile.close()
