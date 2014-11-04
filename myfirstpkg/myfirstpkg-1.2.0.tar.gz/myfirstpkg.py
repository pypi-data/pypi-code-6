def print_lol(mylist, level=0):
  for each_item in mylist:
    if isinstance(each_item, list):
      print_lol(each_item,level+1)
    else:
      for tab_range in range(level):
        print("\t",end='')
      print(each_item)
