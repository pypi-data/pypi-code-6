"""一个嵌套循环打印列表的函数
作者:lmzg
"""
def print_list(the_list,indent=False,level=0):
#传递的三个参数,第二个参数默认为False.为了满足一些人不愿意缩进的意愿
#第三个参数所传递的是:如果使用缩进.那么缩进几位(位以制表符为单位)?默认值是0
    for i in the_list:
        if isinstance(i,list):
            print_list(i,indent,level+1)
        else:
            if indent:
                for num in range(level):
                   print ("\t",end='')
            print (i)
