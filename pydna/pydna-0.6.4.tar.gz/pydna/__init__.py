#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2013,2014 by Björn Johansson.  All rights reserved.
# This code is part of the Python-dna distribution and governed by its
# license.  Please see the LICENSE.txt file that should have been included
# as part of this package.

'''
    Python-dna
    ~~~~~~~~~~

    The Python-dna package.

    :copyright: Copyright 2013,2014 by Björn Johansson. All rights reserved.
    :license:   This code is part of the Python-dna distribution and governed by its
                license.  Please see the LICENSE.txt file that should have been included
                as part of this package.

'''

__version__      = "0.6.4"
__date__         = "2014-07-09"
__author__       = "Björn Johansson"
__copyright__    = "Copyright 2013,2014 Björn Johansson"
__credits__      = ["Björn Johansson", "Mark Budde"]
__license__      = "BSD"
__maintainer__   = "Björn Johansson"
__email__        = "bjorn_johansson@bio.uminho.pt"
__status__       = "Development" # "Production" #"Prototype"

from pydna.amplify                                  import Anneal
from pydna.amplify                                  import pcr
from pydna.assembly                                 import Assembly
from pydna.download                                 import Genbank
from pydna.dsdna                                    import Dseq
from pydna.dsdna                                    import Dseqrecord
from pydna.dsdna                                    import parse
from pydna.dsdna                                    import read
#from pydna.dsdna                                    import glob
from pydna.editor                                   import Editor
from pydna.findsubstrings_suffix_arrays_python      import common_sub_strings
from pydna.primer_design                            import cloning_primers
from pydna.primer_design                            import assembly_primers
from pydna.primer_design                            import primer_pair
from pydna.utils                                    import copy_features
from pydna.utils                                    import eq
from pydna.utils                                    import shift_origin
from pydna.utils                                    import pairwise
from pydna.utils                                    import cseguid


try:
    del findsubstrings_suffix_arrays_python
    del assembly
    del dsdna
    del editor
    del amplify
    del utils
    del download
    del _simple_paths8
    del py_rstr_max
except NameError:
    pass

