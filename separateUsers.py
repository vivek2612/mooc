# Takes a log file as user input.
# Creates a new directory named - userLogs
# For each user, the program pushes the records in the file userLogs/username.

from mylib import *
import os
import sys
import math


files = sys.argv[1]
print files
fname = files

f = open(fname,'r')
lines = f.readlines()
f.close()
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
	f = open(new_dir+"/"+username,'a') 
	f.write(userMap[username])
	f.close()
	# break