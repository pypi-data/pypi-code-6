#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, codecs, base64

"""
Templetize is a script to convert a file or a directory (recursively)
to a template for codegen.

Codegen uses a single jinja2 template from a given file or string and
the data you provide to the code generator to recreate the previously
templetized file structure (maybe with renaming parts of it) and writes
it to stdout.

See the jinja2 documentation for the template syntax.
"""

if __name__ == '__main__':
	if len(sys.argv) == 2:
		print '# code generator template created with templetize from %s' % sys.argv[1]
		for root, dirs, files in os.walk( sys.argv[1] ):
			print '@@@ dir %s' % root
			for file in files:
				try:
					f = codecs.open(root+'/'+file, encoding='utf-8', errors='strict')
					for line in f:
						pass
					print '@@@ file %s' % (root+'/'+file)
					print open(root+'/'+file).read()
				except UnicodeDecodeError:
					print '@@@ binary %s' % (root+'/'+file)
					print base64.b64encode( open(root+'/'+file, 'rb').read() )
	else:
		print >>sys.stderr, "%s <file|dir>" % sys.argv[0]
		print >>sys.stderr, "required argument missing"
