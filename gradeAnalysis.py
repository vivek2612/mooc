from mylib import *
import os
import sys
import math

def readfile(fname):
	f = open(fname,'r')
	lines = f.readlines()
	f.close()
	return lines

def buildGradeMap(fname):
	lines = readfile(fname)
	gradeMap = {}
	for line in lines:
		arr = line.split(",")
		uname = arr[0].strip()
		grade = arr[2].strip()
		if gradeMap.has_key(uname):
			print "Double trouble for "+uname
		gradeMap[uname] = grade
	return gradeMap

def buildProfileMap(fname):
	lines = readfile(fname)
	profileMap = {}
	for line in lines:
		arr = line.split(":")
		profileMap[arr[0].strip()] = eval(arr[1].strip())
	return profileMap


# Example : python gradeAnalysis.py grades/grades-348-699.csv profileCounts/profileCount_15-21Sept 
gradeFile = sys.argv[1]  #csv file containing grades. <Username, Name, Grade> 
profileFile = sys.argv[2] #profileCount file . <username : [1,10,2,5,7] >
gradeMap = buildGradeMap(gradeFile)
profileMap = buildProfileMap(profileFile)

outfile = "cluster-grade-relation-15-21Sept-348-699.csv"
f = open(outfile,'w')
gradeStats = {}
for user in profileMap.keys():
	if gradeMap.has_key(user):
		record = user+", " 
		for count in profileMap[user]:
			record += str(count) + ", "

		if not gradeStats.has_key(gradeMap[user]):
			gradeStats[gradeMap[user]] = [[0]*len(profileMap[user]),0]

		gradeStats[gradeMap[user]][0] =  [ x+y for x,y in zip(profileMap[user], gradeStats[gradeMap[user]][0]) ]
		gradeStats[gradeMap[user]][1] += 1

		record += gradeMap[user] + "\n"
		# print record
		f.write(record)
f.close()


for grade in gradeStats.keys():
	gradeStats[grade] = [((x*1.0)/(1.0*gradeStats[grade][1])) for x in gradeStats[grade][0]] 
	# print grade, "=>", gradeStats[grade]
	# gradeStats[grade] represents average sessions in each cluster. It is a list. 

#take transpose of this data to feed it to table_demo.py i.e. plotting graph
data = np.array(gradeStats.values())
data = np.transpose(data)

# import pprint 
# pprint.pprint(data)
