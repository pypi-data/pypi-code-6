"""一个嵌套循环打印列表的函数
作者:lmzg
"""
def print_list(the_list,level=0):
#传递的两个参数,第二个参数为可选参数.但默认值是0
    for i in the_list:
        if isinstance(i,list):
            print_list(i,level+1)
        else:
            for num in range(level):
                print ("\t",end='')
            print (i)
