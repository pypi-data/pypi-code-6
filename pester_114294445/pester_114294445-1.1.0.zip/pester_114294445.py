def print_wow(the_list,level):
        for each_item in the_list:
                if isinstance(each_item,list):
                        print_wow(each_item,level+1)
                else:
                        for tab_stop in range(level):
                                print("\t",end='')
                        print(each_item)
