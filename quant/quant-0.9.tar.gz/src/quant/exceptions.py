from dm.exceptions import *

class QuantApplicationError(DomainModelApplicationError): pass

class PricerLimitError(QuantApplicationError): pass

