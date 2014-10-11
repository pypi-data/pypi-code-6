# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

try:
    from django.utils import datetime
except:
    from datetime import datetime

try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        from django.utils import simplejson as json

try:
    import xml.etree.ElementTree as ET
except:
    import elementtree.ElementTree as ET
