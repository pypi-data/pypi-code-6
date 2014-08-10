def DS(BaseLength):
        #Call this Method with your desired side-length. It will be increased to (2*SideLength)+1 to fit the algorithm
	import random
	TotalLength = (2*BaseLength)+1
	HeightMap = [[0 for x in range(TotalLength)] for x in range(TotalLength)]

	HeightMap[0][0] = random.random()
	HeightMap[0][TotalLength-1] = random.random()
	HeightMap[TotalLength-1][0] = random.random()
	HeightMap[TotalLength-1][TotalLength-1] = random.random()

	#SetMidPoint
	HeightMap[int((TotalLength-1)/2)][int((TotalLength-1)/2)] = random.random()
	#Set MissingValues
	HeightMap[int((TotalLength-1)/2)][0] = (HeightMap[0][0]+HeightMap[TotalLength-1][0])/2
	HeightMap[0][int((TotalLength-1)/2)] = (HeightMap[0][0]+HeightMap[0][TotalLength-1])/2
	HeightMap[int((TotalLength-1)/2)][TotalLength-1] = (HeightMap[0][TotalLength-1]+HeightMap[TotalLength-1][TotalLength-1])/2
	HeightMap[TotalLength-1][int((TotalLength-1)/2)] = (HeightMap[TotalLength-1][0]+HeightMap[TotalLength-1][TotalLength-1])/2

	SquareStep(0,int((TotalLength-1)/2),0,int((TotalLength-1)/2),HeightMap)
	SquareStep(0,int((TotalLength-1)/2),int((TotalLength-1)/2),TotalLength-1,HeightMap)
	SquareStep(int((TotalLength-1)/2),TotalLength-1,0,TotalLength-1,HeightMap)
	SquareStep(int((TotalLength-1)/2),TotalLength-1,int((TotalLength-1)/2),TotalLength-1,HeightMap)

	#Smoothing missed Slots
	for X in range(TotalLength):
		for Y in range(TotalLength):
			if(HeightMap[X][Y]==0):
				if(X > 0 and X < TotalLength-1):
					HeightMap[X][Y] = (HeightMap[X-1][Y]+HeightMap[X+1][Y])/2
				if(X == 0 and X < TotalLength-1):
					HeightMap[X][Y] = HeightMap[X+1][Y]
				if(X == TotalLength-1 and X > 0):
					HeightMap[X][Y] = HeightMap[X-1][Y]

	return HeightMap

def SquareStep(StartX,EndX,StartY,EndY,HeightMap):
	import math
	if(math.fabs(StartX-EndX) <= 1):
		return
	if(math.fabs(StartY-EndY) <= 1):
		return
	else:
		MidPointValue = (HeightMap[StartX][StartY]+HeightMap[StartX][EndY]+HeightMap[EndX][StartY]+HeightMap[EndX][EndY])/4
		HeightMap[int(((EndX-StartX)/2)+StartX)][int(((EndY-StartY)/2)+StartY)] = MidPointValue
		#New MissingPoints
		#UMid
		HeightMap[int(((EndX-StartX)/2)+StartX)][StartY] = (HeightMap[StartX][StartY]+HeightMap[EndX][StartY]+HeightMap[int(((EndX-StartX)/2)+StartX)][int((EndY-StartY)/2+StartY)])/3
		#RMid
		HeightMap[EndX][int((EndY-StartY)/2+StartY)] = (HeightMap[EndX][StartY] + HeightMap[EndX][EndY] + HeightMap[int(((EndX-StartX)/2)+StartX)][int(((EndY-StartY)/2)+StartY)])/3
		#TMid
		HeightMap[int(((EndX-StartX)/2)+StartX)][EndY] = (HeightMap[int(((EndX-StartX)/2)+StartX)][int(((EndY-StartY)/2)+StartY)] + HeightMap[EndX][EndY] + HeightMap[StartX][EndY])/3
		#LMid
		HeightMap[StartX][int((EndY-StartY)/2+StartY)] = (HeightMap[int(((EndX-StartX)/2)+StartX)][int(((EndY-StartY)/2)+StartY)] + HeightMap[StartX][StartY] + HeightMap[StartX][EndY])/3
		#Assignment of new Quads
		#LUnten
		SquareStep(StartX,int(((EndX-StartX)/2)+StartX),StartY,int(((EndY-StartY)/2)+StartY),HeightMap)
		#RUnten
		SquareStep(int(((EndX-StartX)/2)+StartX),EndX,StartY,int(((EndY-StartY)/2)+StartY),HeightMap)
		#LOben
		SquareStep(StartX,int(((EndX-StartX)/2)+StartX),int(((EndY-StartY)/2)+StartY),EndY,HeightMap)
		#ROben
		SquareStep(int(((EndX-StartX)/2)+StartX),EndX,int(((EndY-StartY)/2)+StartY),EndY,HeightMap)

def PrintHeightMap(HeightMap):
	#PRINTS HEIGHTMAP
	for X in range(len(HeightMap)):
		print("\t")
		for Y in range(len(HeightMap[X])):
			print("    "+str(HeightMap[X][Y]),end="")

