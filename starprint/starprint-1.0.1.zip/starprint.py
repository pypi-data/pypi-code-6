"""like this:
***
**
*
"""
def backStarPrint(x,place=0):
	sp = ''
	for i in range(1,place):
		sp += ' '
	star = '*'
	for i in range(1,x):
		star += '*'
	for i in range(0,x):
		print sp + star
		x -= 1
		star = star[0:x]

"""like this:
*
**
***
"""
def starPrint(x,place=0):
	sp = ''
	for i in range(1,place):
		sp += ' '
	star = '*'
	for x in range(0,x):
		print sp + star
		star += '*'

"""like this:
***
 **
  *
"""
def reverseStarPrint(x,place=0):
	sp = ''
	for i in range(1,place):
		sp += ' '
	star = '*'
	blank = ' '
	for i in range(1,x):		
		blank += ' '
	for i in range(0,x):
		"""print blank + star"""		
		x -= 1
		blank = blank[0:x]
		print sp + blank + star
		star += '*'

"""like this:
  *
 ***
*****
"""
def trianglePrint(x,place=0):
	sp = ''
	for i in range(1,place):
		sp += ' '
	star = '*'
	blank = ' '
	for i in range(1,x):		
		blank += ' '
	for i in range(0,x):		
		x -= 1
		blank = blank[0:x]
		print sp + blank + star
		star += '**'

"""like this:
*****
 ***
  *
"""
def reverseTrianglePrint(x,place=0):
	sp = ''
	for i in range(1,place):
		sp += ' '
	star = '*'
	blank = ''
	for i in range(1,x):
		star += '**'
	for i in range(0,x):
		print sp + blank + star
		blank += ' '
		x -= 1
		star = star[0:2*x-1]
	
"""like this:
*
**
***
**
*
"""
def suoStar(x,place=0):
	starPrint(x,place)
	backStarPrint(x-1,place)

"""like this:
  *
 ***
*****
 ***
  *
"""
def diamond(x,place=0):
	trianglePrint(x,place)
	reverseTrianglePrint(x-1,place+1)
