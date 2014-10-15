import pkgutil
import hyperdns.vendor.drivers as base

# stores the located drivers in a quick dict
driver_registry={}

# this is used to import a driver class, verbosity indicates whether or not
# problems will be reported
def import_driver(vkey,verbose=True):
    """Try to import the driver class given the name, returning None if
    there is an error.  The package hyperdns.vendor.drivers.<vkey> will
    be imported and the class HyperDNSDriver will be loaded
    
    :param str vkey: the vkey of the driver to import
    :param bool verbose: determines if an import error will be printed
    :return: the driver class
    :rtype: HyperDNSDriver class
    """
    try:
        dclass=driver_registry.get(vkey)
        if dclass==None:
            mname='%s.%s' % (base.__name__,vkey)
            mod=__import__(mname,globals(),locals(),['HyperDNSDriver'])
            dclass=getattr(mod,'HyperDNSDriver')
            driver_registry[vkey]=dclass
        return dclass
    except Exception as E:
        if verbose:
            print(E)
        return None

def _auto_discover_drivers():
    """Scan the packages looking for all available drivers.  This is called
    during module init
    """
    for importer, modname, ispkg in pkgutil.iter_modules(base.__path__):
        d=import_driver(modname)
        if d==None:
            print("Failed loading driver %s" % modname)
        else:
            driver_registry[modname]=d

def getAvailableVendorDrivers():
    """return the driver classes of the available vendors"""
    return [d for d in driver_registry.values()]

def getAvailableVendorNames():
    """return the names only of the available vendors"""
    return sorted([d.name for d in driver_registry.values()])

def getAvailableVendorKeys():
    """return the keys only of the available vendors"""
    return sorted([d.vkey for d in driver_registry.values()])

def getAvailableVendorKeyNameTuples():
    """return the (key,name) and keys of the available vendors"""
    return sorted([(d.vkey,d.name) for d in driver_registry.values()])
