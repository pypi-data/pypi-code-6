from scour import scour

'''
Scripting interface for external package Scour
'''

class DictWrap(object):
    # Not written by me! Written by MAJGIS, downloaded from 
    # http://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
    """ Wrap an existing dict, or create a new one, and access with either dot 
      notation or key lookup.
    
      The attribute _data is reserved and stores the underlying dictionary.
      When using the += operator with create=True, the empty nested dict is 
      replaced with the operand, effectively creating a default dictionary
      of mixed types.
    
      args:
        d({}): Existing dict to wrap, an empty dict is created by default
        create(True): Create an empty, nested dict instead of raising a KeyError
    
      example:
        >>>dw = DictWrap({'pp':3})
        >>>dw.a.b += 2
        >>>dw.a.b += 2
        >>>dw.a['c'] += 'Hello'
        >>>dw.a['c'] += ' World'
        >>>dw.a.d
        >>>print dw._data
        {'a': {'c': 'Hello World', 'b': 4, 'd': {}}, 'pp': 3}
    
    """
    
    def __init__(self, d=None, create=True):
        if d is None:
            d = {}
        supr = super(DictWrap, self)  
        supr.__setattr__('_data', d)
        supr.__setattr__('__create', create)
    
    def __getattr__(self, name):
        try:
            value = self._data[name]
        except KeyError:
            if not super(DictWrap, self).__getattribute__('__create'):
                raise
            value = {}
            self._data[name] = value
        
        if hasattr(value, 'items'):
            create = super(DictWrap, self).__getattribute__('__create')
            return DictWrap(value, create)
        return value
    
    def __setattr__(self, name, value):
        self._data[name] = value  
    
    def __getitem__(self, key):
        try:
            value = self._data[key]
        except KeyError:
            if not super(DictWrap, self).__getattribute__('__create'):
                raise
            value = {}
            self._data[key] = value
            
            if hasattr(value, 'items'):
                create = super(DictWrap, self).__getattribute__('__create')
                return DictWrap(value, create)
        return value
    
    def __setitem__(self, key, value):
        self._data[key] = value
    
    def __iadd__(self, other):
        if self._data:
            raise TypeError("A Nested dict will only be replaced if it's empty")
        else:
            return other

def optimize(inputname, outputname, **kwargs):
    '''
    Wrapper to allow scour (external svg optimization program) to be used from script.
    Inputs:
        outputname(str) - name of the outputfile for the optimized svg
        kwargs - must be valid values for the 'dest' attribute in scour._options_parser
            Defaults as follows:
                {'strip_ids': False, 'shorten_ids': False, 'simple_colors': True, 
                 'strip_comments': False, 'remove_metadata': False, 'outfilename': None, 
                 'group_create': False, 'protect_ids_noninkscape': False, 'indent_type': 'space', 
                 'keep_editor_data': False, 'shorten_ids_prefix': '', 'renderer_workaround': True, 
                 'style_to_xml': True, 'protect_ids_prefix': None, 'enable_viewboxing': False, 
                 'digits': 5, 'embed_rasters': True, 'infilename': None, 'strip_xml_prolog': False, 
                 'group_collapse': True, 'quiet': False, 'protect_ids_list': None}
    '''
    # TODO: Fix this hack
    default_options = scour._options_parser.defaults
    for option, value in zip(kwargs.keys(), kwargs.values()):
        default_options[option] = value
    options = DictWrap(default_options)
    svg_optimized = open(outputname, 'w')
    svg = open(inputname, 'r')
    svg_string = svg.read()
    optimized_string = scour.scourString(svg_string, options = options)
    svg_optimized.write(optimized_string)
    svg.close()
    svg_optimized.close()