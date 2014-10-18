import re

def sugar(exclude=[]):
    """build the preprocessor function
    
    Exclude any undesired preprocessors.
    """
    preprocessors = {
        'import': convert_imports,
        'def': convert_defs,
        'call': convert_calls
    }
    for ex in exclude:
        del preprocessors[ex]
    
    def process(text):
        for processor in preprocessors.values():
            text = processor(text)
        return text
        
    return process

def _sub(text, pattern, replace):
    return re.sub(pattern, replace, text, flags=re.MULTILINE)

def convert_imports(text):
    """preprocess short import syntax
    
    Anything starting with a / or $ is a file. Otherwise, assumed to be a module.
    
    Always one of these forms:
    
    import ... as ...
    from ... import ...
    
    """
    
    def import_type(name):
        if name.startswith(('/', '$')):
            return 'file'
        else:
            return 'module'
    
    pattern_import_as = '%\s*import\s*(\S+)\s*as\s*(.*)$'
    def replace_import_as(matchobj):
        (filename, name) = matchobj.groups()
        return '<%%namespace name="%s" %s="%s" />' % \
            (name, import_type(filename), filename)
    
    pattern_import_from = '%\s*from\s*(\S+)\s*import\s*(.*)$'
    def replace_import_from(matchobj):
        (filename, imports) = matchobj.groups()
        return '<%%namespace %s="%s" import="%s" />' % \
            (import_type(filename), filename, imports)
    
    text = _sub(text, pattern_import_as, replace_import_as)
    text = _sub(text, pattern_import_from, replace_import_from)
    return text

def convert_defs(text):
    """preprocess short def syntax"""
    
    pattern_def = '(%\s*def\s+(\S+):\s*$)'
    def replace_def(matchobj):
        (line, expr) = matchobj.groups()
        return '<%%def name="%s">' % expr.strip()    
        
    pattern_end_def = '^\s*%\s*enddef\s*$'
    replace_end_def = '</%def>'
    
    text = _sub(text, pattern_def, replace_def)
    text = _sub(text, pattern_end_def, replace_end_def)
    return text
    
def convert_calls(text):
    """preprocess short call syntax"""
    
    pattern_call = '(%\s*call(.*):\s*$)'
    def replace_call(matchobj):
        (line, expr) = matchobj.groups()
        return '<%%call expr="%s">' % expr.strip()    
    
    pattern_end_call = '^\s*%\s*endcall\s*$'
    replace_end_call = '</%call>'
    
    text = _sub(text, pattern_call, replace_call)
    text = _sub(text, pattern_end_call, replace_end_call)    
    return text
    
    
    
    
    
    
    