"""
1.0.1新增level引數
1.0.2給level預設值,使模組支援二種api(level可填可不填)
"""
def printNext(theList,level=0):
    for eachN in theList:
        if isinstance(eachN,list):
            printNext(eachN,level+1)
        else:
            for tabStop in range(level):
                print("\t",end='')      #end=''不換行
            print(eachN)
