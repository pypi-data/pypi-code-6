#!/usr/bin/env python
"""
Build the combined apipkg from each _sdl_*.renamed
"""

api = ["""# API
import apipkg

nsdict = """, """

apipkg.initpkg(__name__, nsdict, {'__all__':sorted(nsdict.keys())})
"""]

def go():
    import _sdl_ttf.renamed
    import _sdl_mixer.renamed
    import _sdl_image.renamed
    import _sdl.renamed

    import pprint
    import os

    # prefix/mapping pairs
    mappings = [('_sdl.lib', dict(_sdl.renamed._mapping())),
        ('_sdl_mixer.lib', dict(_sdl_mixer.renamed._mapping())),
        ('_sdl_image.lib', dict(_sdl_image.renamed._mapping())),
        ('_sdl_ttf.lib', dict(_sdl_ttf.renamed._mapping()))]

    nsdicts = {}

    for prefix, mapping in mappings:
        nsdicts[prefix] = dict((v, '%s:%s' % (prefix, k)) for k, v in mapping.items())

    nsdict = nsdicts['_sdl.lib']
    nsdict['mixer'] = nsdicts['_sdl_mixer.lib']
    nsdict['image'] = nsdicts['_sdl_image.lib']
    nsdict['ttf'] = nsdicts['_sdl_ttf.lib']

    exports = pprint.pformat(nsdict)

    api_filename = os.path.join(os.path.dirname(__file__), "..", "sdl", "__init__.py")
    with open(api_filename, "w+") as output:
        output.write(exports.join(api))

if __name__ == "__main__":
    go()
