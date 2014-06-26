'''
my utils module
'''

"""
print a list recursively
"""
def printList (itemList):
	for item in itemList:
		if(isinstance(item, list)):
			printList(item)
		else:
			print(item)
