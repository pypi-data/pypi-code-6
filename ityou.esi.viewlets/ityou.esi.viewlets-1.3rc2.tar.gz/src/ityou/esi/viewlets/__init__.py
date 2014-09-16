# -*- coding: utf-8 -*-
from zope.component.hooks import getSite

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

def initialize(context):
    """Initializer called when used as a Zope 2 product."""