def print_wow(the_list,indent=False,level=0):
        for each_item in the_list:
                if isinstance(each_item,list):
                        print_wow(each_item,level+1)
                else:
                        if indent:
                                for tab_stop in range(level):
                                        print("\t",end='')
                        print(each_item)
