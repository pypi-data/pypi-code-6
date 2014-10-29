def print_lolz(the_list):
	for item in the_list:
		if isinstance(item,list):
			print_lolz(item)
		else:
			print "$$", item
