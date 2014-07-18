"""This module will help pint items in list of list.
   Additionaly allowing nested items to be printed 
   with tab stops. 
"""

def print_lol(the_list,indent=False,level=0):
	"""This is a recursive function
	which takes three arguments. 
	First one is a list
	Second is optional switch to turn on/off the indenting of sublists 
	Third is also an optional providing the starting tab value"""	  
	for nested_item in the_list:
		if isinstance(nested_item,list):
			print_lol(nested_item,indent,level+1)
		else:	
			if(indent):
				for tab_stop in range(level):
					print("\t",end="")
			print(nested_item)
