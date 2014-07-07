from zope.component.hooks import getSite
import ityou.thumbnails as me
PRODUCT_PATH = me.__path__[0]
DEFAULT_IMAGES_PATH = PRODUCT_PATH + '/browser/images/'

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