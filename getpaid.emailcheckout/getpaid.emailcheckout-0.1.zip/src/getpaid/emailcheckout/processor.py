"""
"""
from getpaid.emailcheckout.interfaces import IEmailProcessor
from getpaid.emailcheckout.interfaces import IEmailOptions

from zope import interface


from Products.PloneGetPaid.interfaces import IGetPaidManagementOptions
from getpaid.core import interfaces as GetPaidInterfaces



class EmailProcessor(object):

    interface.implements(IEmailProcessor)

    options_interface = IEmailOptions

    def __init__( self, context ):
        self.context = context


    def refund(self, order, amount):
        #XXX what is that for?
        pass

    def capture(self, order, price):
        """we can't check if the customer can pay right now.
        this is done later by our staff
        """
        return GetPaidInterfaces.keys.results_async

    def authorize( self, order, payment ):
        """we need not authorize the payment here
        """
        # payment contains the information (credit card etc) that
        # we did not collect in this processor
        return GetPaidInterfaces.keys.results_success
