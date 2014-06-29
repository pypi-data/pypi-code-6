'''
my utils module
'''

"""
print a list recursively.
control the sublist indent with 'indent'
"""
def printList (itemList, indent = 0):
	for item in itemList:
		if(isinstance(item, list)):
			printList(item, indent + 1)
		else:
			for num in range(indent):
				print('\t', end='')
			print(item)
