import sys
f=open(sys.argv[1],'r')
lines = f.readlines()
outfile=open('feature-activity-mapping.txt','w')
for line in lines:
	arr = line.split(':')
	activity = arr[0].strip()
	allfeatures = eval(arr[1].strip())
	for feature in allfeatures:
		outfile.write(str(feature)+" : "+activity+'\n')
	
f.close()
outfile.close()