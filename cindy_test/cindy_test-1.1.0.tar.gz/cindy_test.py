"""这是nester.py模块，提供函数用来打印循环嵌套列表"""
def print_lol(the_list,level=0,indent=False):
    """这个函数打印一个包含嵌套列表的列表，并tab缩进"""
    for each in the_list:
        if isinstance(each,list):
            print_lol(each,level+1,indent)
        else:
            if indent:
                for num in range(level):
                    print("\t",end='')
            print(each)
