import sys
import os
from mylib import *

current_dir = os.getcwd()
data_dir = current_dir + "/data"

def create_data_dir():
	if not os.path.exists(data_dir):
		os.mkdir(data_dir)

create_data_dir()
fname = sys.argv[1]
f = open(fname,"r")
lines = f.readlines()
prev_date = ""
current_file=""
for line in lines:
	arr = line.split(" ")
	#['vishalds735@gmail.com', '1.187.161.5', '-', '[24/Jun/2014:03:40:07', '+0530]', '', '"GET', '/concept/3/null', 'HTTP/1.1"', '404', '1164', '"http://14.139.97.83/concept/3/"', '"Mozilla/5.0', '(Windows', 'NT', '6.1;', 'rv:31.0)', 'Gecko/20100101', 'Firefox/31.0"', '0.022', '0.022', '.\n']
	date = extract_date(arr[3]) #[24/Jun/2014:03:40:17
	if(prev_date!=date):
		if(current_file!=""):
			current_file.close()
		prev_date = date
		filename = data_dir + "/"+ date
		current_file=open(filename,'w')
	current_file.write(line)
current_file.close()
f.close()