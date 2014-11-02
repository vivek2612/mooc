from mylib import *
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import math


fname = sys.argv[1]

f = open(fname,'r')
lines = f.readlines()
f.close()


krange = []	
betavar = []
cv_intra = []
cv_inter = []
betacv = [] 

# line: K, v_intra, v_inter, coeffVariation_intra, coeffVariation_inter
for line in lines:
	arr = line.split()
	K = int(arr[0].strip())
	v_intra = float(arr[1].strip())
	v_inter = float(arr[2].strip())
	coeffVariation_intra = float(arr[3].strip())
	coeffVariation_inter = float(arr[4].strip())

	krange.append(K)
	betavar += [ v_intra/v_inter ]
	cv_intra += [ coeffVariation_intra ]
	cv_inter += [ coeffVariation_inter ]
	betacv += [ coeffVariation_intra/coeffVariation_inter ]

plt.xticks(krange, krange)
plt.plot(krange, betavar, marker='o', label="Beta Variance")
plt.plot(krange, betavar)
plt.grid()
plt.xlabel("Number of clusters (K)")
plt.title(fname+" : Cluster Analysis")
plt.legend()
plt.show()


plt.xticks(krange, krange)
plt.plot(krange, betacv)
plt.plot(krange, betacv, marker='o',label="Beta-CV")
plt.plot(krange, cv_intra )
plt.plot(krange, cv_intra, marker='o',label="CV Intra")
plt.plot(krange, cv_inter)
plt.plot(krange, cv_inter, marker='o',label="CV Inter")
plt.grid()
plt.title(fname+" : Cluster Analysis")
plt.xlabel("Number of clusters (K)")
plt.legend()
plt.show()
