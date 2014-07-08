# -*- coding: utf-8 -*-

class CreateForm():
    def __init__(self, fields):
        self.fields = dict()
        self.fields['is_error'] = False
        for key in fields.keys():
            self.fields[key] = fields[key]
        self.errors = list()

    def addError(self, item, message, value):
        assert item in self.fields.keys(), "The item '%s' was not found in key's dict" % item
        error = dict()
        error['location'] = item
        error['message'] = message
        error['value'] = value
        self.errors.append(error)

    def getList(self):
        registers = list()
        c = 1
        for error in self.errors:
            register = dict()
            for item in self.fields.keys():
                register[item] = self.fields[item]
            register['cod'] = 'test_%d' % c
            register[error['location']] = error['value']
            register['is_error'] = True
            register['error'] = error
            registers.append(register)
            c += 1
        return registers

