import cStringIO as StringIO
import logging
import xmltodict

logging.basicConfig(level=logging.FATAL)

def loads(__xml):
    dumpedString = xmltodict.parse(__xml)
    return(dict(dumpedString))

def load(file_):
    __xml = None
    with open(file_) as fin:
        __xml = loads(fin.read())
    return(__xml)

def dumps(dictionary):
    __xml = xmltodict.unparse(dictionary)
    return(__xml)

def dump(obj, output):
    __bytes = dumps(obj)
    logging.debug(__bytes)
    with open(output, 'w') as fout:
        fout.write(__bytes)
    return(fout.name)
    

