#coding:utf-8
'''
Created on 07.12.2010

@author: akvarats
'''

from controller import urls_tests_controller

from actions import TestActionPack1, TestActionPack2

def register_actions():
    '''
    '''
    urls_tests_controller.packs.extend([TestActionPack1, TestActionPack2(),])