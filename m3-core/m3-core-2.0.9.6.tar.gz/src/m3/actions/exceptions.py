# -*- coding: utf-8 -*-


class ApplicationLogicException(Exception):
    '''
    Исключительная ситуация уровня бизнес-логики приложения.
    '''

    def __init__(self, message):
        # Это исключение плохо подвергается pickle! пришлось дописать.
        # пруф:
        #   http://bugs.python.org/issue1692335
        #   http://bugs.python.org/issue13751
        Exception.__init__(self, message)
        self.exception_message = message

    def __str__(self):
        return self.exception_message
