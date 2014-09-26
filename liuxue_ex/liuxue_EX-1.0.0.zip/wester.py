def print_lol(the_list):
    """这是一个处理嵌套列表的递归函数"""
    for each_one in the_list:
        if(isinstance(each_one,list)):
            print_lol(each_one)
        else:
            print(each_one)
