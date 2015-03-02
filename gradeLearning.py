"""
Apply linear regression model to learn and predict the grades of the user. 
"""

from mylib import *
from numpy.linalg import inv
import os
import sys
import math

#example : cluster-grade-relation-15-21Sept-348-699.csv
fname = sys.argv[1]  #File containing <username, n1, n2, n3, n4, n5, grade> {ni means number of session in ith cluster}
f = open(fname,'r')
lines = f.readlines()
f.close()
k = len(lines[0].split(',')) - 2 #Number of different types of clusters

gradeValueMap = {'AP': 10, 'AA':10, 'AB':9, 'BB':8, 'BC':7, 'CC':6, 'CD':5, 'DD':4, 'FR':0}

X = [] # each row containing xi
Y = [] # the grade
for line in lines:
	arr = line.split(',')
	grade = arr[-1].strip()
	if(grade=='AU'):
		continue
	Y.append(gradeValueMap[grade])
	arr = [int(value) for value in arr[1 : 1+k]]
	X.append(arr)

X = np.matrix(X)
Xt = np.transpose(X)
Y = np.transpose(np.matrix(Y))

W = inv(Xt*X)*Xt*Y   # minimizing ||XW - Y||^2 w.r.t W
print W




