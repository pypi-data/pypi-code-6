# -*- coding: utf-8 -*-

"""
CSV Cleaner

>>> import csvcleaner
>>> f = csvcleaner.CSVCleaner('path/to/file.csv')

(c) 2014 by Palmer Group Media, LLC.
Apache 2.0, see LICENSE for more details.
"""

__title__ = 'csvcleaner'
__description__ = 'Removes rows containing blacklisted words from a CSV file.'
__version__ = '1.0.6'
__author__ = 'James C. Palmer'
__email__ = 'james@pgmny.com'
__url__ = 'https://github.com/palmer/csvcleaner'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2014 Palmer Group Media, LLC'


from .csvcleaner import CSVCleaner
