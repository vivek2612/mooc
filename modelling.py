from mylib import *
import os
import sys
import math

fname = sys.argv[1] # file with logs of only single user
lines = readFile(fname)

prevtime = 0
for line in lines:
	arr = getArray(line)
	timeArr = getTime(arr)

	timeInMin = timeInMinutes(timeArr)
	if timeInMin < prevtime:
		timeInMin += 24*60	# for cases like when 23:59 and then 00:02. So add 24*60.
	prevtime = timeInMin

