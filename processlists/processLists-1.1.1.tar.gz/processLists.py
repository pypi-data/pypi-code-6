""" Module test sorting list with nested lists"""

def procList(alist,level=0):
	if(level == 0):
		for i in alist:
			if isinstance(i,list):
				procList(i,0)
			else:
				print(i)
	else:
		for i in alist:
			if isinstance(i,list):
				procList(i,level+1)
			else:
				for j in range(level-1):
					print('\t',end='')
				print(i)


"""function is recursive and can go to any level of nesting default is 100
if the user enters a none zero value for the function tabbed printing of
the list and sub lists is invoked, zero value flatterns the list"""