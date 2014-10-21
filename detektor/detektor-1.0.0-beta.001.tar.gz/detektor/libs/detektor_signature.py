
class DetektorSignature:
    """ A class holding the attributes that are used as signature. """

    def __init__(self, *args, **kwargs):
        self.keywordstring = kwargs.get('keywordstring')
        self.operatorstring = kwargs.get('operatorstring')
        self.bigstring = kwargs.get('bigstring')
        self.bigstringhash = kwargs.get('bigstringhash')
        self.number_of_keywords = kwargs.get('number_of_keywords')
        self.number_of_operators = kwargs.get('number_of_operators')
        self.list_of_functions = kwargs.get('list_of_functions')

    def __repr__(self):
        return u"""Keywords: {}
Operators: {}
Bigstring: {}
Bigstringhash: {}
Number of keywords: {}
Number of operators: {}
Functions: {}""".format(
            self.keywordstring, self.operatorstring, self.bigstring,
            self.bigstringhash, self.number_of_keywords,
            self.number_of_operators, self.list_of_functions)
