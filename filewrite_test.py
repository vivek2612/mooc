def writetofile(filename, arr):
	f = open(filename, 'a')
	f.write(str(arr)+"\n")
	f.write("Written")
	f.close()

arr = [[1,2],[2,3]]
filename = "filewrite_test_file";
f = open(filename,'w')
f.close()
writetofile(filename, arr)
writetofile(filename, arr)
