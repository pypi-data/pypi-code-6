"""
1.0.1新增level引數
1.0.2給level預設值,使模組支援二種api(level可填可不填)
1.0.3加入第三個引數，讓使用者決定是否啟動空格功能
"""
def printNext(theList,indent=False,level=0,fh=sys.stdout):   # fh是由sketch_save.py的例子引用新加入引數
    for eachN in theList:
        if isinstance(eachN,list):
            printNext(eachN,indent,level+1,fh)
        else:
            if indent:
                for tabStop in range(level):
                    print("\t",end='',file=fh)      #end=''不換行
            print(eachN,file=fh)
