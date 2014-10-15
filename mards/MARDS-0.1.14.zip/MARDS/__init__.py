# MARDS\__init__.py
#
# MARDS data serialization library
#
__version__ = '0.1.14'
__version_info__ = tuple([ int(num) for num in __version__.split('.')])

MARDS_VER_CURRENT = "1.0" # this is the SPEC version, NOT the library version

from rolne import rolne
import os

import standard_types as st
import mards_library as ml
import doc

def string_to_rolne(string, schema=None, schema_file=None):
    global MARDS_VER_CURRENT
    schema_dir = os.getcwd()
    if schema_file:
        with open(schema_file, "r") as fh:
            schema = fh.read()
            schema_dir = os.path.dirname(os.path.realpath(schema_file))
    if not schema:
        schema = "#!MARDS_schema_en_"+MARDS_VER_CURRENT+"\n    exclusive false\n"
    return ml.MARDS_to_rolne(doc=string, schema=schema, schema_dir=schema_dir)

def string_to_python(doc=None, schema=None, context="doc", tab_strict=False):
    r, error_list = MARDS_to_rolne(doc, schema, context=context, tab_strict=tab_strict)
    if schema:
        schema, schema_errors = MARDS_to_rolne(schema, context="schema")
        error_list.extend(schema_errors)
        result = ml.sub_convert_python(r, schema)
    else:
        result = r.dump()
    return result, error_list

def compile(doc_rolne, schema=None, schema_file=None, schema_rolne=None, renumber=False):
    global MARDS_VER_CURRENT
    schema_errors = []
    if type(doc_rolne) is not rolne:
        raise TypeError, "first parameter must be a rolne"
    if not schema_rolne:
        schema_dir = os.getcwd()
        if schema_file:
            with open(schema_file, "r") as fh:
                schema = fh.read()
                schema_dir = os.path.dirname(os.path.realpath(schema_file))
        if not schema:
            schema = "#!MARDS_schema_en_"+MARDS_VER_CURRENT+"\n    exclusive false\n"
        schema_rolne, schema_errors = ml.SCHEMA_to_rolne(schema, prefix="", schema_dir=schema_dir)
    copy = doc_rolne.copy(seq_prefix="", renumber=renumber)
    new_rolne, doc_errors = ml.schema_rolne_check(copy, schema_rolne)
    all_errors = schema_errors + doc_errors
    return new_rolne, all_errors
    
def rolne_to_string(r, tab_size=4, quote_all=True):
    result = ""
    #print r.data
    if r:
        for (rn, rv, rl, rs) in r.data:
            result += rn
            if rv is not None:
                printable = str(rv)
                quote_flag = False
                if '"' in printable:
                    quote_flag = True
                if len(printable) != len(printable.strip()):
                    quote_flag = True
                if quote_flag or quote_all:
                    result += " "+'"'+rv+'"'
                else:
                    result += " "+rv
            result += "\n"
            if rl:
                temp = rolne_to_string(rolne(in_list=rl), tab_size=tab_size, quote_all=quote_all)
                for line in temp.split("\n"):
                    if line:
                        result += " "*tab_size+line
                        result += "\n"
    return result

if __name__ == "__main__":

    print "TBD"
