#!/usr/bin/env python

import os.path, textwrap, json, sys

try:
    import StringIO
except:
    from io import StringIO

from lxml.etree import XSLT, XML, parse, tostring

DEBUG=False

def get_dox(dox_file):
    """Use XSLT to parse certain documentation out of doxygen xml."""
    dox = parse(dox_file)
    with open("dox.xsl", "r") as transform_file:
        transform = XSLT(parse(transform_file))

    result = transform(dox)
    return result

def reformat(result):
    """Line wrap etc. from XSLT-transformed documentation."""
    funcdocs = {}
    for funcdef in result.xpath(".//function"):
        if not funcdef.text: continue
#         if DEBUG:
#             print funcdef.text
        sio = StringIO.StringIO()
        last_line = ''
        for line in funcdef.text.splitlines():
            line = line.lstrip()
            if not line:
                continue
            if not (last_line.startswith(':') and line.startswith(':')):
                if not (last_line.startswith('*  ') and line.startswith('*  ')):
                    sio.write("\n")
            if line.startswith('*'): # code examples
                sio.write(' ' + line[1:])
            else:
                subsequent_indent = '' if not line.startswith(':') else '    '
                sio.write('\n'.join(textwrap.wrap(line,
                                                  subsequent_indent=subsequent_indent)))
            sio.write('\n')
            last_line = line
        funcdocs[funcdef.attrib['name']] = sio.getvalue()
    return funcdocs

all_funcdocs = {}

base_path = sys.argv[1]
for a, b, files in os.walk(base_path):
    for filename in files:
        if not filename.endswith('.xml'): continue
        with open(os.path.join(a, filename), "r") as dox_file:
            gathered_dox = reformat(get_dox(dox_file))
            all_funcdocs.update(gathered_dox)

with open('dox.json', 'w+') as dox_out:
    json.dump(all_funcdocs, dox_out, indent=2)
    # print all_funcdocs['SDL_CreateWindow']
    # print all_funcdocs['SDL_WarpMouseInWindow']
