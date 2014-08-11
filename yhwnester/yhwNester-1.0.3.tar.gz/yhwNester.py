"""
1.0.1新增level引數
1.0.2給level預設值,使模組支援二種api(level可填可不填)
1.0.3加入第三個引數，讓使用者決定是否啟動空格功能
"""
def printNext(theList,indent=False,level=0):
    for eachN in theList:
        if isinstance(eachN,list):
            printNext(eachN,indent,level+1)
        else:
            if indent:
                for tabStop in range(level):
                    print("\t",end='')      #end=''不換行
            print(eachN)
