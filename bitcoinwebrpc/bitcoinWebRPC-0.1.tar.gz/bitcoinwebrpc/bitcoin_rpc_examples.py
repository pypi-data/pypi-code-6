"""
getbalance 
getconnectioncount
getinfo
getpeerinfo
getreceivedbyaccount
getreceivedbyaddress
gettransaction
listaddressgroupings
listreceivedbyaccount
listreceivedbyaddress
setaccount
settxfee
stop
validateaddress
"""

import bitcoin
from json_proxy import RawProxy
import os

#bitcoin rpc , reads conf automatically
rp = RawProxy()
print rp
r = rp._call('getinfo')
print r

print rp._call('getbalance')

print rp._call('getpeerinfo')

print rp._call('listaddressgroupings')

print rp._call('listreceivedbyaddress')
