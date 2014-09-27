"""this is a module to print all the list member nested at any level"""
def prin(listy,level):
 for each in listy:
  if isinstance(each,list):
   prin(each,level+1)
  else:
   for num in range(level): 
    print("\t",end='')
   print(each)   

