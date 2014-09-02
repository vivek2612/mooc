#!/bin/bash
dir="Desktop/Test18/"
logfile=$dir"simplifiedlogs.txt"
videofile=$dir"video_objects.txt"
jsfile=$dir"js.txt"
GETfile=$dir"GET.txt"
POSTfile=$dir"POST.txt"
cssfile=$dir"css.txt"

saveflag=$1 #First argument of this bash file is saveflag

python clientBandwidth.py $logfile $saveflag
python pie.py $logfile $saveflag
python reqSizeDistribution.py $videofile video $saveflag
python reqSizeDistribution.py $jsfile js $saveflag
python reqSizeDistribution.py $cssfile css $saveflag
python reqSizeDistribution.py $POSTfile post $saveflag
python videoPopularity.py $videofile $saveflag
python viewership.py $logfile $saveflag
python userLevel.py $logfile $saveflag 

# python videos-per-day.py $videofile $saveflag #the video file doesn't have a username

