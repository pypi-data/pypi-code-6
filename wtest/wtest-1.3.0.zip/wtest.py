#第二章
#函数转换为模块1.3.0，完善版
#创建一个名为nester.py模块文件，内容包含第一章的函数代码
#用内置函数range()让嵌套列表缩进指定数目的制表符
'''提示：要使用print() BIF在屏幕上显示一个制表符（TAB），而不是简单换行（这是print()的默认行为），
需要使用以下Python代码：print("\t",end='')。'''
"""（三重引号是多行注释开始）这是“nester.py”模块，提供了一个名为print_lol()的函数，这个函数
的作用是打印列表，其中有可能包含（也可能不包含）嵌套列表。（三重引呈是多行注释结束）
2、第二个参数（名为“level”）用来在遇到嵌套列表时插入制表符。
为“level”增加一个缺省值使得“level”变成一个可选参数。
3、为函数增加第三个参数。将这个参数命名为indent,开始时这个参数值设置为False－－－也就是说，默认
情况下不打开缩进特性。在函数体中使用indent值来控制实现缩进的代码"""
def print_lol(the_list,indent=False,level=0):
    """这个函数取一个位置参数，名为“the_list”，这可以是任何Python列表（也可以是包含嵌套的列表）
。所指定的列表中的每个数据项会（递归地）输出到屏幕上，各数据项各上一行。"""
    for lol_ab in the_list:
        if isinstance(lol_ab,list):
            #1、增加level参数的目的就是为了能控制嵌套输出。每次处理一个嵌套列表时，都需要将level的值增加1
           #2、签名已经改变，所以一定要将参数indent更新到这里调用
            print_lol(lol_ab,indent,level+1)
        else:
            #一个简单的“if”语句就可以达到目的，不要忘记"if"代码行未尾的:冒号
            if indent:
            #使用“level”的值来控制使用多少个制表符。
                for tab_stop in range(level):
                #每一层缩进显示一个TAB制表符
                    print('\t',end='')
            print(lol_ab)
            
################以下为调用函数说明################
#print_lol(movies,2)     #调用函数，并提供两个参数，第二个参数为另一个起始值
#print_lol(movies)   #调用函数，提供一个参数，第二个参数使用缺省值
#print_lol(movies,True,0) #调用函数，并提供三个参数，不过第二个参数为真（True），第三个参数提供为默认值
