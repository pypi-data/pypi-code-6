# Generate SDL_image wrappers.
# Only used at build time.

import os
import re
from .builder import Builder

header = """# Automatically generated wrappers.
# Override by adding wrappers to helpers.py.
from .dso import ffi, _LIB
from .structs import unbox, Struct
from _sdl.structs import u8
from _sdl.autohelpers import SDL_version

"""

def go():
    from _sdl_mixer import cdefs
    builder = Builder()
    output_filename = os.path.join(os.path.dirname(__file__),
                                   "..",
                                   "_sdl_mixer",
                                   "autohelpers.py")
    with open(output_filename, "w+") as output:
        output.write(header)
        builder.generate(output,
                         cdefs=cdefs,
                         helpers=cdefs,
                         filter=re.compile("^.* (Mix_|MIX_).*$"))

if __name__ == "__main__":
    go()
