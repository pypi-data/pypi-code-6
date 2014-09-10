"""Main product initializer
"""
from logging import getLogger
from zope.i18nmessageid import MessageFactory


plonedemograficoMessageFactory = MessageFactory('pd.plonedemografico')
plonedemograficoLogger = getLogger('pd.plonedemografico')


def initialize(context):
    ''' Initialize this product
    '''
