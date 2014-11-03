#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple


# Variables ===================================================================


# Functions & objects =========================================================
class ExportRequest():
    def __init__(self, aleph_record, book_id, filename, b64_data):
        self.aleph_record = aleph_record
        self.book_id = book_id
        self.filename = filename
        self.b64_data = b64_data


class ExportResult():
    def __init__(self, export_id, exported):
        self.export_id = export_id
        self.exported = exported


class ExportTrackingRequest():
    def __init__(self, book_id):
        self.book_id = book_id


class TrackingStates():
    def __init__(self, exported, error):
        self.exported = exported
        self.error = error


class ExportTrackingResult():
    def __init__(self, book_id, state):
        self.book_id = book_id
        self.state = state
