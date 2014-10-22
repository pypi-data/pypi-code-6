names = ["Jair", ["Alice", "Yuting", "Ya"]]

def print_lol(the_list, level = 0):
	for each_item in the_list:
		if(isinstance(each_item, list)):
			print_lol(each_item, level + 1)
		else:
			for count in range(level):
				print("\t", end='')
			print(each_item)

print_lol(names, 0)
print_lol(names)
print_lol(names, 2)
