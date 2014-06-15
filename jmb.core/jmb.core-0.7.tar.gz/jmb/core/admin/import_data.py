# coding: utf-8
"""
Import Data
===========
"""

import re
import os
import sys
import email
import tempfile
import datetime

from django.conf import settings

from jmb.core.utils.data_import import XlsFile


class ImportData(XlsFile):
    def __init__(self, model, filename=None, file_contents=None, auto=False, sheet_index=0, *args, **kwargs):
        super(ImportData, self).__init__(filename=filename, file_contents=file_contents, auto=auto, sheet_index=sheet_index)
        self.model = model
        self.fields_map = self.get_fields_map()
        self.messages = {}
        self.messages['inserted']=0
        self.messages['modified']=0
        self.messages['errors']=[]

    def get_fields_map(self):
        # {'id': 'id', 'fields1': 'fields1', ...}
        field_names = self.model._meta.get_all_field_names()
        fields_map = {}
        for name in field_names:
            key = name
            try:
                field = self.model._meta.get_field(name)
                field_type = field.get_internal_type()
            except:
                pass

            # if field is ForeignKey
            if field_type == "ForeignKey":
                key += "_id"

            fields_map[key] = name
        return fields_map

    def do(self, row, kw, j):
        inserted = False
        modified = False
        id = row.id

        try:
            record, created = self.model.objects.get_or_create(id=row.id, defaults=kw)
            if created:
                self.messages['inserted'] += 1
            else:
                self.messages['modified'] += 1
            record.save()
        except Exception, e:
            self.messages['errors'].append('riga %s - codice: %s: %s' %(j, row.codcli, e))