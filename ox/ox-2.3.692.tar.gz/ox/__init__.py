# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# GPL 2011
try:
    from . import __version
    __version__ = __version.VERSION
except:
    __version__ = '2.3.692'

from . import cache
from . import js
from . import jsonc
from . import net
from . import srt
from . import utils

from .api import *
from .file import *
from .form import *
from .format import *
from .geo import *
from .html import *
#image depends on PIL, not easy enough to instal on osx
try:
    from .image import *
except:
    pass
from .location import *
from .movie import *
from .normalize import *
from .oembed import *
from .text import *
#currently broken in python3
try:
    from .torrent import *
except:
    pass
from .fixunicode import *
