'''dossier.fc Feature Collections

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2014 Diffeo, Inc.

'''

from __future__ import absolute_import, division, print_function

import pytest

from dossier.fc.feature_collection import registry

@pytest.fixture(params=filter(lambda k: 'Counter' in k, registry.types()))
def counter_type(request):
    return registry.get_constructor(request.param)
