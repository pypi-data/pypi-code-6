def printList(theList, levelIndent):
    for cada_item in theList:
        if isinstance(cada_item,list):
            printList(cada_item, levelIndent+1)
        else:
            for tab_stop in range(levelIndent):
               print("\t", end='')
               print(cada_item + "<-")

    

                        


