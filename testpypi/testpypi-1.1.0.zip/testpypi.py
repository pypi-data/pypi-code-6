def print_list(the_list,level):
    for i in the_list:
        if isinstance(i,list):
            print_list(i,level+1)
        else:
            for num in range(level):
                print ("\t",end='')
            print (i)
