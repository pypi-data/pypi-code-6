

# 
#       The connection class provides methods for a client to establish a network connection to
#       a server, and for both peers to operate the connection thereafter.
#     
# 
#       connection          = open-connection *use-connection close-connection
#       open-connection     = C:protocol-header
#                             S:START C:START-OK
#                             *challenge
#                             S:TUNE C:TUNE-OK
#                             C:OPEN S:OPEN-OK
#       challenge           = S:SECURE C:SECURE-OK
#       use-connection      = *channel
#       close-connection    = C:CLOSE S:CLOSE-OK
#                           / S:CLOSE C:CLOSE-OK
#     

from Start import Start
from StartOk import StartOk
from Secure import Secure
from SecureOk import SecureOk
from Tune import Tune
from TuneOk import TuneOk
from Open import Open
from OpenOk import OpenOk
from Close import Close
from CloseOk import CloseOk

