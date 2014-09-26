import sys
def print_lol (the_list,indent=False,deep=0,fn=sys.stdout):
        for each_item in the_list:
                if isinstance(each_item,list):
                        print_lol(each_item,indent,deep+1,fn)
                else:
                        if indent:
                                print("\t" *deep,end="",file=fn)
                        print(each_item,file=fn)
