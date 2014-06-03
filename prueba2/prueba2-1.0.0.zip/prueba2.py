def printList(theList):
	for xx in theList:
		if isinstance(xx,list):
			printList(xx)
		else:
			print(xx)


