   

def function (names,indent=False,level=0):

    for each_name in names:
        if isinstance (each_name,list ):
            function(each_name,indent,level+1)
        else:
            if indent:
                for tab_stop in range (level):
                      print("\t",end=' ')
            print(each_name)
                        


                
