# -*- coding: utf-8 -*-
# :Progetto:  PatchDB -- PatchingRST
# :Creato il: Fri Oct  3 00:37:54 2003
# :Autore:    Lele Gaifax <lele@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

from __future__ import absolute_import


def setup(app):
    "Setup the Sphinx environment."

    if not hasattr(app, 'add_config_value'):
        # Silly nosetests!
        return

    from .script import setup as setup_script

    # This is the pickle where we store the found scripts, at the
    # end of the build
    app.add_config_value('patchdb_storage', None, False)

    setup_script(app)
