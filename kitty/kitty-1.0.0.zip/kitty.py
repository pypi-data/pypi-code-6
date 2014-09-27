"""this is a module to print all the list member nested at any level"""
def prin(listy):
 for each in listy:
  if isinstance(each,list):
   prin(each)
  else:
   print(each)   

