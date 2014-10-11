

# 
#       Exchanges match and distribute messages across queues. Exchanges can be configured in
#       the server or declared at runtime.
#     
# 
#       exchange            = C:DECLARE  S:DECLARE-OK
#                           / C:DELETE   S:DELETE-OK
#     

from Declare import Declare
from DeclareOk import DeclareOk
from Delete import Delete
from DeleteOk import DeleteOk

