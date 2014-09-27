"""this is a module to print all the list member nested at any level"""
def prin(listy,ident=False,level=0):
 for each in listy:
  if isinstance(each,list):
   prin(each,ident,level+1)
  else:
   if ident:
    for num in range(level): 
     print("\t",end='')
   print(each)   

