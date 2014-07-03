def men_lol(the_list,indent=False,level=0,xy=sys.stdout):
	for mens in the_list:
		if isinstance(mens,list):
			men_lol(mens,indent,level+1i,xy)
		else:
			if indent:
				for tab_shop in range(level):
					print("\t",end='',file=xy)
			print(mens,file=xy)
