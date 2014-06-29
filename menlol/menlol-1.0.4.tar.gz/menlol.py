def men_lol(the_list,indent=False,level=0):
	for mens in the_list:
		if isinstance(mens,list):
			men_lol(mens,indent,level+1)
		else:
			if indent:
				for tab_shop in range(level):
					print("\t",end='')
			print(mens)
