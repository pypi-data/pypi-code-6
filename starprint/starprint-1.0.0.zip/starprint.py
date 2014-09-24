def backStarPrint(x):
	star = '*'
	for i in range(1,x):
		star += '*'
	for i in range(0,x):
		print star
		x -= 1
		star = star[0:x]

def starPrint(x):
	star = '*'
	for x in range(0,x):
		print star
		star += '*'


def suoStar(x):
	starPrint(x)
	backStarPrint(x-1)


