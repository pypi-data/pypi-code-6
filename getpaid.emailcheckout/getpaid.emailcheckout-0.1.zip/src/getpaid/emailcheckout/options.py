
from getpaid.core.options import PersistentOptions
from getpaid.emailcheckout.interfaces import IEmailOptions


EmailOptions = PersistentOptions.wire("EmailOptions",
                                      "getpaid.emailcheckout",
                                      IEmailOptions)

