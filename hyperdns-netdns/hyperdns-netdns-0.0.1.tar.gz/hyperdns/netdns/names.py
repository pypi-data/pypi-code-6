

def dotify(name):
    """ Add a dot to the end of the name if it wasn't there.
    """
    if not name.endswith("."):
        return "%s." % name
    return name

def undotify(name):
    if name.endswith("."):
        return name[:-1]
    return name


def fqdn(name,zone=None):
    """ This produces a string version of a name that is dot terminated
        and ends with the trailing zone.  If the name already ends with
        the zone name, it is not appended.  For example

            (a) -> a.
            (a.) -> a.
            (a,example.com) -> a.example.com.
            (a.example.com,example.com) -> a.example.com.

        the return value is ascii, not unicode

        Note: does not detect multi
    """
    # ensure trailing dot
    if not name.endswith('.'):
        # add zone if required, ensuring dot
        if zone==None:
            name+='.'
        else:
            if not zone.endswith('.'):
                if name.endswith(zone):
                    name=name+'.'
                else:
                    name=name+'.'+zone+'.'
            else:
                name+='.'
                if not name.endswith(zone):
                    name=name+zone

    return name

def splitHostFqdn(name,zone=None):
    """ split a name into two parts, if a zone is specified then we
        will append that to the end of the name if required.
    """
    f=fqdn(name,zone)
    components=f.split(".")[:-1]
    ct=len(components)
    if ct<2:
        raise Exception("'%s' is not a host or zone fqdn" % name)
    elif ct==2:
        return (None,'.'.join(components)+'.')
    else:
        return ('.'.join(components[:-2]),'.'.join(components[-2:])+'.')




                    


