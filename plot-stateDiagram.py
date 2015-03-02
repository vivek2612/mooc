# -*- coding: utf-8 -*-
"""
pydot example 2
@author: Federico Cáceres
@url: http://pythonhaven.wordpress.com/2009/12/09/generating_graphs_with_pydot
"""
from globalmaps import *
from mylib import *
import os
import sys
import math
import pydot

graph = pydot.Dot(graph_type='digraph',splines= 'spline'	)

colors = ["blue", "green", "purple", "red", "cyan", "magenta", "black", "orange", "brown"]
idToState = {}
for key,val in stateList.items():
	idToState[val] = key

def addNodes(graph):
	for state in idToState.values():
		nd = pydot.Node(state,color=colors[stateList[state]], fill=True)
		graph.add_node(nd)	

fname = sys.argv[1]  # file with final centroids written. 
f = open(fname,'r')
lines = f.readlines()
count=0;
for line in lines:
	mat = eval(line)
	graph = pydot.Dot(graph_type='digraph',splines= 'spline')
	addNodes(graph)
	for i in range(len(stateList)):
		for j in range(len(stateList)):
			if(mat[i][j]>0.1):
				graph.add_edge(pydot.Edge(pydot.Node(idToState[i]), pydot.Node(idToState[j]), label=mat[i][j],color=colors[i%9]))
	graph.write_png(str(count)+'stategraph.png')
	count+=1

f = open('state-diagram.html','w')
f.write("<html><body>");
for i in range(count):
	f.write("<h1>User Profile #"+str(i+1)+"</h1>")
	f.write("<img src='"+str(i)+'stategraph.png'+"'/>")
f.write("</body>")
f.write("</html>")


