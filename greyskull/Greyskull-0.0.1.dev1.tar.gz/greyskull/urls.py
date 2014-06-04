# -*- coding: utf-8 -*-

import os

from tornado.web import URLSpec

from greyskull.handlers import (NTrack,
                                BTCompat,
                                MemStat,
                                Index,
                                Redirect, )

urlpatterns = [
    URLSpec(r'/ntrk/(.*)', NTrack, kwargs=dict(port=os.getenv('GREYSKULL_EXTERNAL_PORT', 80),
                                               stats=os.getenv('GREYSKULL_STATS', True),
                                               errors=os.getenv('GREYSKULL_ERRORS', True),
                                               interval=os.getenv('GREYSKULL_INTERVAL', 18424))),
    URLSpec(r'/tracker', BTCompat),
    URLSpec(r'', MemStat),
    URLSpec(r'/', Index),
    URLSpec(r'.*', Redirect),
]
