from getpaid.core import interfaces
from zope import schema


class IEmailProcessor(interfaces.IPaymentProcessor):
    """
    Email Checkout Processor
    """

class IEmailOptions(interfaces.IPaymentProcessorOptions):
    """
    Email Checkout Options
    """
