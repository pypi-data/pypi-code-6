def print_lol(the_list, level):
    for movie in the_list:
        if isinstance(movie, list):
            print_lol(movie, level+1)
        else:
            for tab in range(level):
                print("\t",end='')
            print(movie)
