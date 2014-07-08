# -*- coding: utf-8 -*-
import logging
from zope.component.hooks import getSite

TRANSLATION = {
               "today"      : "Heute",
               "yesterday"  : "Gestern",
               "never"      : "nie",
               }

def isProductAvailable(product):
    """Check if a product is installed and return True, 
    else return False
    """
    qui = getSite().portal_url.getPortalObject().portal_quickinstaller
    installed_products = qui.listInstalledProducts()
    for prod in installed_products:
        if prod["id"] == product and prod["status"] == "installed":
            return True
    return False