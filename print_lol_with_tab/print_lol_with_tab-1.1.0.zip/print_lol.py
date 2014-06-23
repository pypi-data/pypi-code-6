def print_lol (the_list, level = 0, indent = False):
  for item in the_list:
    if isinstance (item, list):
      print_lol (item, level + 1, indent)
    else:
      if indent == True:
        print ("\t" * level, end = "")
      print (item)

a_list = ["Fire",["Fox",["is",["a",["great",["man",["!"]]]]]]]
print_lol (a_list)
print_lol (a_list, 0, True)
