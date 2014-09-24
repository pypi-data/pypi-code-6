#coding:utf-8
'''
Created on 20.01.2011

@author: kir
'''
from django.shortcuts import render_to_response
from m3.ui.actions import Action, ActionPack

class CheckIE6(Action):
    '''
    Заглушка для IE6
    Возвращает страничку с информацией, и предложением скачать актуальные браузеры
    '''
    url = '/ie6'
    def run(self, request, context):
        return render_to_response('check_ie6.html')
        

class CheckBrowserActionsPack(ActionPack):
    '''
    Набор действий для проверки браузеров
    '''
    def __init__(self):
        super(self.__class__,self).__init__()
        self.actions.append(CheckIE6())
        