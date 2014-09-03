# Generate libSDL2 wrappers.

import json
import os.path
import pprint

from .builder import Builder

header = """# Automatically generated wrappers.
# Override by adding wrappers to helpers.py.
from .dso import ffi, _LIB
from .structs import Struct, unbox, SDLError, u8

"""

api = ["""# API
import apipkg

exports = """, """

ns_dict = dict((s, '_sdl.renamed:%s' % s)
               for s in exports if not s.startswith('_'))
ns_dict['image'] = '_sdl_image.renamed'
ns_dict['mixer'] = '_sdl_mixer.renamed'
ns_dict['ttf'] = '_sdl_ttf.renamed'

apipkg.initpkg(__name__, ns_dict, {'__all__':exports})
"""]


def go():
    from _sdl import cdefs, helpers

    try:
        with open(os.path.join(os.path.dirname(__file__), 'dox.json'), 'r') as funcdocs:
            all_funcdocs = json.load(funcdocs)
    except IOError:
        all_funcdocs = {}

    builder = Builder(all_funcdocs)

    output_filename = os.path.join(os.path.dirname(__file__),
                                   "..",
                                   "_sdl",
                                   "autohelpers.py")
    with open(output_filename, "w+") as output:
        output.write(header)
        builder.generate(output, cdefs=cdefs, helpers=helpers)

    import _sdl.renamed

    exports = pprint.pformat(sorted(name for name in dir(_sdl.renamed)
                                    if not name.startswith('_')))
    api_filename = os.path.join(os.path.dirname(__file__), "..", "sdl", "__init__.py")
    with open(api_filename, "w+") as output:
        output.write(exports.join(api))

if __name__ == "__main__":
    go()
