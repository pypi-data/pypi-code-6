# coding: utf-8
"""
.. _data_import:

Importare dati
==============

Questo modulo fornisce alcune classi per facilitare l'importazione di dati da file excel e csv
Si suppone che ogni file sia composto da fogli :class:`.Sheet`

Un esempio di importazione sarà::


    from jmb.organization.models import Contact
    from jmb.core.utils.data_import import XlsFile

    class Anagrafiche(XlsFile):
        fields_map = {
            'code' : 'ancodice',
            'description' : 'andescri',
            'foo' : 'antipcon',
          }
        def do(self, row, kw):
             # modi alternativi di referenziare i dati
             Contact.objects.get_or_create(code=row.ancodice, defaults=kw)
             #Contact.objects.get_or_create(code=kw['code'], defaults=kw)

    x = Anagrafiche('anagrafiche.xls', auto=True)
    x.read()

field_list
-----------

un metodo semplice di dare il nome alle colonne è di impostarlo con 
l'attributo :attr:`Sheet.field_list`, le colonne possono poi essere mappate 
in field names tramite :attr:`Sheet.fields_map`



.. autoclass:: Sheet
   :members: field_list, fields_map, read, do, handle_exception

xls
----

.. autoclass:: XlsFile
   :members:

csv
----

.. autoclass:: CsvFile
   :members:


"""
import re
import datetime
from collections import namedtuple
#import csv

import unicodecsv as csv

# Ogg = namedtuple('Ogg', ",".join(attributes))
import xlrd

class Sheet(object):
    """
    Abstract sheet
    """
    #: a list of field names. Optional. When present it will be used
    #: to name each column instead of looking at the column header.
    #: Field name here is the row attribute (eg: row.first_name)
    field_list = None
    
    #: a dict mapping field names to column headers, as an example, if field_name
    #: has {'first_name' : 'Nome'} it means that :meth:`read` will set::
    #:
    #:   kw['first_name'] = row.Nome


    fields_map = None

    #: Fields listed in this list will be set None if empty
    #: specifically needed to prevent unique problems
    nullable_field_list = None

    def read(self, limit=0, start=0):
        """Loop on all rows of a sheet

        :param start: start reading at line nr. ``start``
        :param limit: limit number of rows to read to ``limit``
        """
        Row = namedtuple('Row', ",".join(self.field_list))
        values = {}
        j = 0
        for line in self.get_rows():
            j += 1
            if j < start:
                continue
            if limit and j >= limit + start:
                break
            row = self.get_tuples_from_row(Row, line)
            kw = self.get_new_dict(row)
            try:
                self.do(row, kw, j)
            except Exception, e:
                self.handle_exception(e, row, kw, j)

    def handle_exception(self, e, row, kw, j):
        """Handle exception of the execution of :meth:`do`
        """
        print "ERROR: row: %s - error: %s" % (j, e)
        
    def setup(self):
        """Setup env possibly used in self.do"""
        return

    def get_fk_as_dict(self, model, value='id', key='name'):
        """Return a dict of all values of a (possible) fk as dict
        
        :param model: the django db model
        :param value: the field to use as value of the dict (default ``id``)
                      Note: will be lowered
        :param key: the field to use as key of the dict (defaykt ``name``)
        """
        values = {}
        qs = model.objects.all()
        for id, name in qs.values_list(value, key):
            values[name.lower()] = id
        return values


    def get_new_dict(self, row):
        
        if not self.fields_map:
            return {}
        row_dict = {}
        for key, val in self.fields_map.iteritems():
            try:
                row_dict[key] = getattr(row, val)
            except AttributeError, e:
                msg = "'%s' is not a correct value, choices are: %s" % (val, vars(row).keys())
                raise AttributeError(msg)

        for field_name in self.nullable_field_list:
            if not row_dict[field_name]:
                row_dict[field_name] = None
        return row_dict

    def get_rows(self,sheet_index=None, sheet=None):
        return NotImplementedError

    def do(self, row, kw, j):
        """implement here your import

        :param row: a namedtuple. Names are the names in the original columns
        :param kw: a dict suitable to feed ``defaults`` keyword attribute of
                   ``get_or_create`` if fields_map is provided::

                     def do(self, row, kw):
                         Contact.objects.get_or_create(cod=row.cod, defaults=kw)

        :param j: integer 1-based counting read rows
        """
        print values


    def clean_field_name(self, value):
        """Clean each column heading to make it a suitable field_name.
        By default strip empty spaces, non ascii chars, parenthesis
        :param value: the column header
        """
        return re.sub('[\s\(\)\.\W]', '', value)

class XlsFile(Sheet):

    data_rows_index = 0
    def __init__(self, filename=None, file_contents=None, auto=False, sheet_index=0):
        """
        :param filename: the cvs file to open
        :param auto_fields: (boolean) se True, i nomi delle colonne saranno 
                         desunti dalla prima riga
        :param sheet_index: indice del foglio da usare (default: 0)
        """

        try:
            if filename:
                self.book = xlrd.open_workbook(filename)
            if file_contents:
                self.book = xlrd.open_workbook(file_contents=file_contents)
        except IOError, e:
            print e
            raise
        self.sheet = self.book.sheet_by_index(sheet_index)
            
        if auto:
            sheet = self.book.sheet_by_index(sheet_index)
            self.field_list = self.get_field_list(sheet.row(0))
            self.data_rows_index = 1
        self.setup()
        self.nullable_field_list = self.nullable_field_list or []

    def xls2csv(self):
        "Really poor version of csv file"
        output = []
        for i in self.get_sheets_as_list():
            output += [";".join([unicode(x.value) for x in i])]
        return "\n".join(output)

    def get_sheet_as_list(self, sheet_name=None, all_sheets=True):
        "get  named sheet or all sheets"
        rows = []
        if sheet_name:
            try:
                sheet = self.book.sheet_by_name(sheet_name)
            except Exception, e:
                raise

            rows += self.get_rows(sheet)

        elif all_sheets is True and sheet_name is None:
            for index in range(self.book.nsheets):
                sheet = self.book.sheet_by_index(index)
                rows += self.get_rows(sheet)
        else:
            sheet = self.book.sheet_by_index(0)
            rows += self.get_rows(sheet)

        return rows

    def get_rows(self, sheet_index=0, sheet=None):
        """
        :param sheet_index: the index of the sheet to read
        :param sheet: a possible sheet object as returned by sheet_by_index
        """
        if not sheet:
            sheet = self.book.sheet_by_index(sheet_index)
        rows = []
        for nrow in range(self.data_rows_index, sheet.nrows):
            yield sheet.row(nrow)

    def xldate2date(self, cell):
        "Returna un datetime.date dal valore della cella"
        assert cell.ctype == 3
        return datetime.date(*xlrd.xldate_as_tuple(cell.value, 0)[0:3])
        
    def get_tuples_from_row(self, Row, row):
        """
        :param Row: typename
        :param row: iterable
        """
        return Row._make(self.get_cell_value(cell) for cell in row)

    def get_cell_value(self, cell):
        """Return the best guess for the correct value"""
        if cell.ctype == 0:    # empty cell
            return ''
        if cell.ctype == 1:    # string
            return cell.value.strip() 
        elif cell.ctype == 2:  # float
            return cell.value
        elif cell.ctype == 3:  # date/datetime
            return self.xldate2date(cell)
        elif cell.ctype == 4:  
            return bool(cell.value)

    def get_field_list(self, row):
        if self.field_list:
            return self.field_list
        return [self.clean_field_name(self.get_cell_value(cell)) for cell in row]

class CsvFile(Sheet):
    
    def __init__(self, filename, auto=False, delimiter=";"):
        """
        :param filename: the cvs file to open
        :param auto_fields: (boolean) se True, i nomi delle colonne saranno 
                         desunti dalla prima riga
        :param delimiter: delimitatore di campi (default ``,``)
        """
        self.reader = csv.reader(open(filename, "rb"), delimiter=delimiter)

        if auto:
            self.field_list = self.get_field_list(self.reader.next())
        self.setup()
        self.nullable_field_list = self.nullable_field_list or []

    def get_tuples_from_row(self, Row, row):
        """
        :param Row: typename
        :param row: iterable
        """
        return Row._make(row)

    def get_rows(self):
        return self.reader

    def get_field_list(self, row):
        if self.field_list:
            return self.field_list
        field_list = [self.clean_field_name(f.strip()) for f in row]
        return field_list
        

if __name__ == '__main__':

    
    simple = '''"nome", "cognome", "eta"
    mario, rossi, 1
    nicola, di bari, 2
    eufrasio, nibionno
    manca, il campo, 
    '''
    tab = """nome	 cognome	 eta
    mario	 rossi	 1
    nicola	 di bari	 2
    eufrasio	 nibionno
    manca	 il campo	 
    """
    import sys
    import os

    def get_file(txt):
        filename = "/tmp/k.csv"
        f = open(filename, "w")
        f.write(txt)
        f.close()
        return filename
    
    if len(sys.argv)> 1:
        filename = sys.argv[1]

    class MyPage(Page):
        def do(self, **values):
            print values['eta']
            
#     p = MyPage(filename=get_file(simple), delimiter=",", auto=True)
#     p.read()
    
    p = MyPage(filename=get_file(tab), delimiter="\t", auto=True)
    p.read()
    
    
