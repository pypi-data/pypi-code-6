                        
"""this is a eaxmple of print out every element in list"""
def print_it(the_list,tabf=False,level=0): 
        for each_item in the_list:
                if isinstance(each_item,list):
                        print_it(each_item,tabf,level+1)
                else:
                        if tabf:
                                for tab in range(level):
                                    print("\t",end='')
                        print(each_item)
cast=["zhao","qian","sun","li",["zhou jia","wu yi",["zheng bing wu"]]]
print_it(cast,1,0)
