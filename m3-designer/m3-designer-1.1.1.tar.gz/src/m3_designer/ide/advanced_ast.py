# coding:utf-8
'''
Created on 14.04.2011

@author: prefer
'''

import ast

class StringSpaces(ast.AST):
    '''
    Добавляет строки с пробелами
    '''
    def __init__(self, lines=1):
        self.lines = lines
