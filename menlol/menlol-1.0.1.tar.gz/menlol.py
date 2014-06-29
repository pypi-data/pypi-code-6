def men_lol(the_list):
	for mens in the_list:
		if isinstance(mens,list):
			men_lol(mens)
		else:
			print(mens)

