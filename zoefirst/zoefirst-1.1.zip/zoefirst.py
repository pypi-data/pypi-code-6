# -*- coding: UTF-8 -*-
def print_lol(var, level):
    for each in var:
        if isinstance(each, list):
            print_lol(each, level + 1)
        else:
            #先打印制表符
            for stop in range(level):
                print('\t', end='')
            print(each)
