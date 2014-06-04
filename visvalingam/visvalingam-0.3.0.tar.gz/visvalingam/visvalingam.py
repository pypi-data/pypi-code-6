#!/usr/bin/python
#This script was written by Ralf Klammer, 24.10.2013
#Re-Implementation of Visvalingam-Wyatt-Algorithm
#basically inspired by these descriptions: http://bost.ocks.org/mike/simplify/

#Simple Maths:
#http://de.wikipedia.org/wiki/Dreiecksfl%C3%A4che
#http://www.serlo.org/math/wiki/article/view/abstand-zweier-punkte-berechnen

import math

class VisvalingamSimplification:
	def __init__(self, line_):
		self.line = line_
		self.indizes = []
		for i in xrange(len(self.line)):
			self.indizes.append(i)
		self.enriched = False

	#calculate the area of one triangle
	def getTriangleArea(self, prevP_, P_, nextP_):
		#get the points of the triangle
		prevP = prevP_
		P = P_
		nextP = nextP_
		#calculate the triangle sites
		a = math.sqrt(pow(float(prevP[0])-float(P[0]),2)+pow(float(prevP[1])-float(P[1]),2))
		b = math.sqrt(pow(float(P[0])-float(nextP[0]),2)+pow(float(P[1])-float(nextP[1]),2))
		c = math.sqrt(pow(float(nextP[0])-float(prevP[0]),2)+pow(float(nextP[1])-float(prevP[1]),2))
		#calculate the area of the triangle
		s = (a+b+c)/2.0
		area_0 = s*(s-a)*(s-b)*(s-c)
		area_0 = abs(area_0)
		area=math.sqrt(area_0)
		return area

	#add the area of the triangle to each point
	def enrichPoints(self):
		minArea = float("infinity");
		for i in range(1,len(self.indizes)-1):
			this = self.indizes[i]
			prev = self.indizes[i-1]
			next = self.indizes[i+1]
			area=self.getTriangleArea(self.line[prev], self.line[this], self.line[next])
			#reset minim value for area, if current is smaller than all previous
			if(area<minArea):
				minArea=area
			#save the area of the triangle as 3rd coordinate
			if(len(self.line[this])<3):		#add if it does not exist
				self.line[this].append(area)
			else:							#replace if it does exist already
				self.line[this][2] = area
		return minArea

	#check for smallest triangles and remove corresponding points from index
	def removeSmallestAreaIndex(self, minArea):
		newIndizes = []
		# print len(self.indizes)
		for i in range(1,len(self.indizes)-1):
			index = self.indizes[i]
			if(self.line[index][2]>minArea):
				newIndizes.append(index)
		newIndizes.insert(0,self.indizes[0])
		newIndizes.append(self.indizes[len(self.indizes)-1])
		self.indizes = newIndizes
		#return newIndizes

	#do Visvalingam-Calculations until only start-& endpoint are left
	def enrichLineString(self):
		while(len(self.indizes)>2):
			minArea_ = self.enrichPoints()
			self.removeSmallestAreaIndex(minArea_)
		self.enriched = True

	#simplify a linestring corresponding to a given tolerance (depends on projection of data)
	def simplifyLineString(self, tolerance_):
		tolerance = tolerance_
		#it is enough to enrich the line once
                minArea_ = self.enrichPoints()
                self.removeSmallestAreaIndex(minArea_)
		#build the new line
		newLine = []
		for p in self.line:
			if(len(p)>2):
				if(p[2]>tolerance):
					newLine.append(p)
			else:
				newLine.append(p)
		#print len(newLine)
		return newLine
