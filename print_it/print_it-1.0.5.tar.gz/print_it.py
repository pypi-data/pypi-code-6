                        
"""this is a eaxmple of print out every element in list"""
def print_it(the_list,tabf=False,level=0,fh=sys.stdout):
        #tabf=table function default close
        for each_item in the_list:
                if isinstance(each_item,list):
                        print_it(each_item,tabf,level+1,fh)
                else:
                        if tabf:
                                for tab in range(level):
                                    print("\t",end='',file=fh)
                        print(each_item,file=fh)

