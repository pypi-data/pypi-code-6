"""     这是我的第一个测试
        功能是打印列表
其中可能包含（也可能不包含）嵌套列表"""
def print_lol (the_list, level = 0):
    for each in the_list:
        if isinstance(each,list):
            print_lol (each, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each)
