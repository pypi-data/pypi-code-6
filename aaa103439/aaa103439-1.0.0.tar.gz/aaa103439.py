def print_lol(the_list):
    for item1 in the_list:
        if isinstance(item1, list):
            print_lol(item1)
        else:
            print item1
