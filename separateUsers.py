from mylib import *
import os
import sys
import math

sessionDurationThreshold = 30	#in minutes;
# i.e. if the diff between prev request and next request is > threshold then,  it's a new session.


files = sys.argv[1]
print files
fname = files

lines = readFile(fname)
createIpUserMap(lines)

userMap={}
prevtime = 0
for line in lines:
	arr = getArray(line)
	username = str(getUsername(arr))
	if username=="-":
		print "username should not have been '-'. Exiting...\n"
		exit(0)
	
	if not userMap.has_key(username):
		userMap[username]=''
	userMap[username] += line

current_dir = os.getcwd()
new_dir = current_dir + "/"+"userLogs"
if not os.path.exists(new_dir):
	os.mkdir(new_dir)

for username in userMap.keys():
	f = open(new_dir+"/"+username,'w')
	f.write(userMap[username])
	f.close()
	# break