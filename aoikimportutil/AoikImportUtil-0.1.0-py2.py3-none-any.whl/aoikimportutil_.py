# coding: utf-8
"""
File ID: 3ngd7IH
"""

import imp
import os.path
import sys

def import_module_by_name(name):
    """import a module by name in Python namespace.
    
    @param name: module name in Python namespace.
    """
    #/
    try:
        return sys.modules[name]
    except KeyError:
        pass
    
    #/
    __import__(name)
    ## raise ImportError if the module not exists.
    ## raise any error from the imported module.
    
    #/
    return sys.modules[name]

def import_module_in_dir(
    ns_dir,
    mod_name,
    ):
    """import a module from a specified namespace dir.
    
    @param ns_dir: path of a namespace dir.
    Namespace dir means the dir is considered as if it's listed in PYTHONPATH.
    
    @param mod_name: name of a module to load from the specified namespace dir.
    The name is in Python namespace, not in filesystem namespace.
    The name is not limited to top-level, both |a| and |a.b.c| are allowed.
    """
    #/
    mod_file_name_s = mod_name.split('.')
    ## |file_name| means the bare name, without extension.
    ##
    ## E.g. 'a.b.c' to ['a', 'b', 'c']
    
    #/
    parent_mod_name = '' ## change in each iteration below
    
    mod_file_dir = ns_dir ## change in each iteration below

    for mod_file_name in mod_file_name_s:
        #/
        if parent_mod_name == '':
            parent_mod_obj = None
            
            mod_name = mod_file_name
        else:
            parent_mod_obj = sys.modules[parent_mod_name]
            
            mod_name = parent_mod_name + '.' + mod_file_name
        
        #/
        if parent_mod_obj:
            __import__(mod_name)
            
            mod_obj = sys.modules[mod_name]
        else:
            file_handle = None
            
            try:
                #/
                tup = imp.find_module(mod_file_name, [mod_file_dir])
                ## raise ImportError

                #/
                mod_obj = imp.load_module(mod_name, *tup)
                ## raise any error from the imported module.

                #/
                file_handle = tup[0]
            finally:
                if file_handle is not None:
                    file_handle.close()

        #/
        parent_mod_name = mod_name
        
        mod_file_dir = os.path.join(mod_file_dir, mod_file_name)

    #/
    return mod_obj

def import_module_by_path(path):
    """import a top-level module by file path.
    
    @param path: path of a module file.
    """
    #/
    ns_dir, mod_file_name = os.path.split(path)
    
    #assert os.path.isdir(ns_dir)

    #/
    mod_name, _ = os.path.splitext(mod_file_name)
    
    #/ ensure the module name has no dot in it
    ##  because it will be loaded as top level
    assert mod_name.find('.') == -1

    #/
    mod_obj = import_module_in_dir(ns_dir, mod_name)

    #/
    return mod_obj

def getattr_chain(obj, attr_chain, sep='.'):
    """get the last attribute of a specified chain of attributes from a specified object.
    
    @param obj: an object
    @param attr_chain: a chain of attribute names
    @param sep: separator for the chain of attribute names 
    """
    #/
    if sep is None:
        sep = '.'

    #/
    attr_name_s = attr_chain.split(sep)

    #/
    new_obj = obj

    for attr_name in attr_name_s:
        new_obj = getattr(new_obj, attr_name)

    #/
    return new_obj

def load_obj(
    obj_uri,
    mod_attr_sep='::',
    attr_chain_sep='.',
    get_mod=False,
    ):
    """
    @param obj_uri: an uri specifying which object to load.
    An |obj_uri| consists of two parts: |module uri| and |attr chain|,
     e.g. |/a/b/c.py::x.y.z| or |a.b.c::x.y.z|

    #/ module uri
    |/a/b/c.py| or |a.b.c| is the |module uri| part.
    Can be either a file path or a module name in Python namespace.
    Whether it is a file path is determined by whether it ends with |.py|.

    #/ attr chain
    |x.y.z| is attribute chain on the module object specified by module uri.

    @param mod_attr_sep: separator between module uri and attr chain.
    
    If |mod_attr_sep| is not present in |obj_uri|,
     consider |obj_uri| as module uri, without attr chain,
     return module object loaded.
    
    @param attr_chain_sep: separator for the chain of attribute names.
    
    @get_mod: whether return the module object along with the attribute object.
    """
    #/
    obj_uri_part_s = obj_uri.split(mod_attr_sep, 2)
    ## use |split| instead of |partition| to be compatible with Python 2.4-
    
    if len(obj_uri_part_s) == 2:
        mod_uri, attr_chain = obj_uri_part_s
    else:
        mod_uri = obj_uri_part_s[0]
        
        attr_chain = None

    #/
    if mod_uri.endswith('.py'):
    ## This means it is a file path, e.g. |/a/b/c.py|
        #/
        mod_file_path = mod_uri

        #/
        mod_obj = import_module_by_path(mod_file_path)
        ## raise error

    else:
    ## This means it is a module name, e.g. |a.b.c|
        #/
        mod_name = mod_uri

        #/
        mod_obj = import_module_by_name(mod_name)
        ## raise error

    #/
    if not attr_chain:
        if get_mod:
            return mod_obj, None
        else:
            return mod_obj

    #/
    #assert attr_chain
    
    attr_obj = getattr_chain(
        obj=mod_obj,
        attr_chain=attr_chain,
        sep=attr_chain_sep,
    )
    ## raise error
    
    #/
    if get_mod:
        return mod_obj, attr_obj
    else:
        return attr_obj
