#!/usr/bin/env python

from .extractor import Extractor
from . import site

def console_main(*args, **conf):
    # site.names

    for url in args:
        # url preprocessing, redirection...
        #extraction = Extractor(url, **conf)

        #site.youku.extractor().download_by_url(url, **conf)
        site.youtube.extractor().download_by_url(url, **conf)
