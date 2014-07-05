# encoding: utf-8
'''
File: localizable.py
Author: Oliver Zscheyge
Description:
    Localizable super class for metrics, rules and reports.
'''

class Localizable(object):
    """Common interface for Metrics, Rules and Reports.
    """
    def __init__(self, ID, language, brief, description):
        super(Localizable, self).__init__()
        self.ID = ID
        self.language = language
        self.brief = brief
        self.description = description

