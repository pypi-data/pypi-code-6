#!/usr/bin/env python
from ldappagedsearch import LdapPagedSearch

def myCallback(dn,record):
    print dn, record


url             = 'ldap://your.ldap.server'
username        = 'username'      # for anything but active directory
username        = 'domain\\user'  # for active directory
password        = 'yourPassword'

baseDN          = 'dc=company,dc=com'
searchFilter    = '(&(objectCategory=user))'

# Preferred

with LdapPagedSearch(url, username, password, maxPages=2, pageSize=2 ) as l:
    l.search(baseDN, searchFilter, callback = myCallback)

# Also Works

l = LdapPagedSearch(url, username, password, maxPages=2, pageSize=2 )
l.search(baseDN, searchFilter, callback = myCallback)
