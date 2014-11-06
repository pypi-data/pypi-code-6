"""this is my module with my functions"""

def print_lol(the_list, level):
    """First example function"""
    for each_item in the_list:
      if isinstance(each_item, list):
        print_lol(each_item,level+1)
      else:
        for tab_stop in range(level):
            print('\t', end='')
        print(each_item)            
def suma(x,y):
  return x+y
