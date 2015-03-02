import matplotlib.pyplot as plt

filename = 'data2'
f = open(filename,'r')
lines = f.readlines()
f.close()

cpuUsage = {}
count = 1.0
for line in lines:
	arr = line.split()
	# time = count + (float)((arr[1].split(':')[2]).split('.')[1])
	print arr[1]
	print "hellow"
	# print time