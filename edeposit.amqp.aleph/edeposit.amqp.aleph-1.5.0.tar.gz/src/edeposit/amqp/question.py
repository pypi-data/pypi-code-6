#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from aleph import *


# Variables ===================================================================
isbn1 = "80-85979-67-1"
isbn2 = "978-80-85979-67-1"


# Main program ================================================================
if __name__ == '__main__':
    print reactToAMQPMessage(SearchRequest(ISBNQuery(isbn1, "e-dep")), "UUID")
    print reactToAMQPMessage(SearchRequest(ISBNQuery(isbn2, "cze-dep")), "UUID")
