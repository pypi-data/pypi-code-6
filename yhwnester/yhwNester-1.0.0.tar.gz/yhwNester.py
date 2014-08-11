"""
1.0.1版新增level引數
"""
def printNext(theList,level):
    for eachN in theList:
        if isinstance(eachN,list):
            printNext(eachN,level+1)
        else:
            for tabStop in range(level):
                print("\t",end='')      #end=''不換行
            print(eachN)
