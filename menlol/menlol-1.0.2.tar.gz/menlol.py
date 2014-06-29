def men_lol(the_list,level):
	for mens in the_list:
		if isinstance(mens,list):
			men_lol(mens,level+1)
		else:
			for tab_shop in range(level):
				print("\t",end='')
			print(mens)
