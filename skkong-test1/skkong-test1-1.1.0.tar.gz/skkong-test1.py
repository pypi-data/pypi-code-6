"""This file is test"""

def print_lol(the_list, level = 0):
	for mov in the_list:
		if isinstance(mov, list):
			print_lol(mov, level+1)
		else:
			for num in range(level):
				print('\t', end='')
			print(mov)
