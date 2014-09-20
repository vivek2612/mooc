#!/bin/bash
logfile=$1  
username=$2 

outputfile=users/$username
cat $logfile |  awk '$3 == var {print $0}' var="$username" > $outputfile
python test.py $outputfile
