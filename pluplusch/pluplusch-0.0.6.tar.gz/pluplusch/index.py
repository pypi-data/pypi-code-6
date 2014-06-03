from importlib import import_module

softwares = ['ckan','opendatasoft','socrata']

def submodules(softwares = softwares):
    return {software: import_module('pluplusch.%s' % software) for software in softwares}

def catalogs(submodules = submodules(softwares)):
    for software, module in submodules.items():
        for catalog in getattr(module, 'catalogs'):
            schemes, rest_of_url = catalog
            for scheme in schemes:
                yield scheme + '://' + rest_of_url, software

def catalog_to_software(catalog, lookup = {}):
    # If the catalog is an iterable of (catalog, software), just return it.
    if len(catalog) == 2:
        return catalog[1]

    if lookup == {}:
        lookup.update(catalogs(submodules(softwares)))

    if catalog in lookup:
        return lookup[catalog]
    else:
        if catalog.startswith('http'):
            msg = "I don't know the software that \"%s\" uses." % catalog
        else:
            msg = "I don't know \"%s\"; try adding \"https://\" or \"http://\" in front of the URL." % catalog
        raise ValueError(msg)

def all_catalogs(submodules = submodules(softwares)):
    for software, module in submodules.items():
        for catalog in getattr(module, 'catalogs'):
            schemes, rest_of_url = catalog
            yield schemes[0] + '://' + rest_of_url
