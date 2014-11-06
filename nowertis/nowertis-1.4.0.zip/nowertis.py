"""this is my module with my functions"""

def print_lol(the_list,indent=False, level=0, fh=sys.stdout):
    """First example function"""
    for each_item in the_list:
      if isinstance(each_item, list):
        print_lol(each_item,indent, level+1, fh)
      else:
            if indent:
                for tab_stop in range(level):
                    print('\t', end='', file=fh)
            print(each_item, file=fg)            
def suma(x,y):
  return x+y
