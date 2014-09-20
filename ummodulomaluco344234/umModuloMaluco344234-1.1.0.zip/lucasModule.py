def teste(myList):
    for item in myList:
        if isinstance(item, list):
            teste(item)
        else:        
            print(item)
