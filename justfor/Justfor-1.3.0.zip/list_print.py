def print_lol (the_list,indent=False,deep=0):
        for each_item in the_list:
                if isinstance(each_item,list):
                        print_lol(each_item,indent,deep+1)
                else:
                        if indent:
                                print("\t" *deep,end="")
                        print(each_item)
