'''
jsonl:  JSON loader which overrides the default JSON module's load and loads methods.
The result is either a mutable object or immutable collections.namedtuple containing
  the JSON's dictionary keys as named attributes, and the dictionary values as the
  attribute's values - much like javascript !
Caveats: Attributes cannot start with an underscore, they can start with an integer
  (under certain conditions) but access to this attribute will only be possible by
  using getattr() symantics - it's best to avoid integer keys anyway.
The following basic types are supported:
  String, list, dict, boolean, None.
A key value of 'None' OR 'null' will yield a json string of 'null'
Mutable object (on load) contain other mutable objects or the basic types (as above),
  they can then have mutable, immutable or other basic types assigned as one of their
  attributes - refer to test/test_jsonl.py.
'''

import simplejson as json

from jsonl import _jsonl as jsonl

jsonl.__doc__ = ''.join([json.__doc__, __doc__])
jsonl.__name__ = __name__
jsonl.__package__ = __name__
jsonl.__path__ = __path__

import sys
sys.modules[__name__] = jsonl
