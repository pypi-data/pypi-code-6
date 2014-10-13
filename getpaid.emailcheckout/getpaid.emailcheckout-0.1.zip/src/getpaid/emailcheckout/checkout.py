from zope import interface
from Products.PloneGetPaid.preferences import DefaultFormSchemas
from Products.PloneGetPaid.browser.checkout import CheckoutReviewAndPay


class IUserPaymentInformation(interface.Interface):
    """we don't need credit card information for our processor
    so we define an empty interface.
    """

    pass



class FormSchemas(DefaultFormSchemas):

    interfaces = dict(DefaultFormSchemas.interfaces)
    interfaces['payment']=IUserPaymentInformation

# XXX maybe it's better to still have all attributes on the bags
# so we don't overrite them by now
#    bags = dict(DefaultFormSchemas.bags)
#    bags['contact_information']=ContactInfo


class CustomCheckoutReviewAndPay(CheckoutReviewAndPay):

    def customise_widgets(self,fields):
        """we don't have any fields we need custom widgets for
        """
        pass