# -*- coding: UTF-8 -*-
def print_lol(var, indent = false, level = 0):
    for each in var:
        if isinstance(each, list):
            print_lol(each, indent, level + 1)
        else:
            if indent:
            #先打印制表符
                for stop in range(level):
                    print('\t', end='')
            print(each)
