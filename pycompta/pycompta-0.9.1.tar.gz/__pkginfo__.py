# -*- coding: utf-8 -*-

# Copyright (c) 2000-2014 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for details.

# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

"""
pycompta packaging information
"""

import os.path as osp
from glob import glob

modname = 'pycompta'
numversion = (0, 9, 1)
version = '.'.join([str(num) for num in numversion])

license = 'GPL'
copyright = '''Copyright (c) 2000-2014 LOGILAB S.A. (Paris, FRANCE).
http://www.logilab.fr/ -- mailto:contact@logilab.fr'''

author = 'Nicolas Chauvat'
author_email = 'Nicolas.Chauvat@logilab.fr'

short_desc = "comptabilité d'entreprise"
long_desc = "comptabilité d'entreprise lisant des fichiers d'écritures au "  \
            "format XML\net produisant des journaux, grand livre, balance, " \
            "compte de résultat\net bilan en XML, ensuite rendus en HTML, "  \
            "XSL:FO et PDF"

web = "http://www.logilab.org/projects/%s" % modname
ftp = "http://ftp.logilab.org/pub/%s" % modname
mailinglist = "mailto://management-projects@lists.logilab.org"

def list_files(directory, pattern):
    root = osp.dirname(__file__)
    return list(osp.join(directory,osp.basename(name))
                for name in glob(osp.join(root, directory, pattern)))

data_files = [['share/pycompta/xml', list_files('doc/xml', '*.xml')],
              ['share/pycompta/xsl', list_files('xsl', '*.xsl')+list_files('xsl', '*.xslt')],
              ['share/pycompta/js', list_files('js', '*.js')],
              ]

scripts = [osp.join('bin', 'pycompta')]

pyversions = ['2.5', '2.6']

