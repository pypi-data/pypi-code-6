

# 
#       Queues store and forward messages. Queues can be configured in the server or created at
#       runtime. Queues must be attached to at least one exchange in order to receive messages
#       from publishers.
#     
# 
#       queue               = C:DECLARE  S:DECLARE-OK
#                           / C:BIND     S:BIND-OK
#                           / C:UNBIND   S:UNBIND-OK
#                           / C:PURGE    S:PURGE-OK
#                           / C:DELETE   S:DELETE-OK
#     

from Declare import Declare
from DeclareOk import DeclareOk
from Bind import Bind
from BindOk import BindOk
from Unbind import Unbind
from UnbindOk import UnbindOk
from Purge import Purge
from PurgeOk import PurgeOk
from Delete import Delete
from DeleteOk import DeleteOk

