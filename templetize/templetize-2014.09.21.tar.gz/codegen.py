#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, jinja2, codecs, base64

"""
Code generator reads and evaluates templates generated with templetize
and creates the directories and files according to the templates
instructions.

Bevore operating the template will be parsed thru jinja2.

See the jinja2 documentation for the template syntax.

Code generator special directives start with "@@@" and extend to the
end of the line. There are 3 different commands. An example:

@@@ dir dir/to/be/generated/

@@@ file dir/to/be/generated/with-a-file-{{inside}}.txt
This is the content {{inside}} of the file. The word inside will be
replaced by jinja2. So if you set 'inside': 'to-generate', you will get
a file called `dir/to/be/generated/with-a-file-to-generate.txt` with
the content `This is the content to-generate of the file. [...]`

@@@ binary another/dir/image.png
IyEvdXNyL2Jpbi9lbnYgcHl0aG9uCiMgLSotIGNvZGluZzogdXRmLTggLSotCgppbXB==

Code generator will not throw exceptions but just ignore already
existing files. They won't be overwritten. A message is printed to
stdout.
"""

def codegen(template_string, data):
	template = jinja2.Template(template_string)
	output = template.render( **data )
	parts = output.split('@@@')[1:]
	for part in parts:
		control = part.split('\n')[0].split(' ')
		if control[1] == 'dir':
			if os.path.isdir(control[2]):
				print >>sys.stderr, "dir %s already exists. ignored." % control[2]
			else:
				os.mkdir(control[2])
		elif control[1] == 'file':
			if os.path.isfile(control[2]):
				print >>sys.stderr, "file %s already exists. ignored." % control[2]
			else:
				f = open(control[2], "w")
				f.write('\n'.join(part.split('\n')[1:]))
				f.close()
		elif control[1] == 'binary':
			if os.path.isfile(control[2]):
				print >>sys.stderr, "binary %s already exists. ignored." % control[2]
			else:
				f = open(control[2], "wb")
				f.write( base64.b64decode( '\n'.join(part.split('\n')[1:]) ) )
				f.close()
