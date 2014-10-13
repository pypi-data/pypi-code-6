"""Common configuration constants
"""
from Products.DataGridField import Column, SelectColumn, DateColumn, DatetimeColumn, \
    DatetimeLocalColumn, FileColumn, EmailColumn, ColorColumn, PasswordColumn, \
    RangeColumn, MonthColumn, SearchColumn, TimeColumn, UrlColumn, WeekColumn

try:
    from Products.DataGridField import LinesColumn
    HAS_LINES_COLUMN = True
except ImportError:
    # BBB as soon as DGF 1.7 is out
    HAS_LINES_COLUMN = False

PROJECTNAME = "PFGDataGrid"

ADD_CONTENT_PERMISSION = 'PloneFormGen: Add Content'

SUPPORTED_COLUMN_TYPES_MAPPING = dict()
SUPPORTED_COLUMN_TYPES_MAPPING['String'] = Column
SUPPORTED_COLUMN_TYPES_MAPPING['Date'] = DateColumn
SUPPORTED_COLUMN_TYPES_MAPPING['Datetime'] = DatetimeColumn
SUPPORTED_COLUMN_TYPES_MAPPING['DatetimeLocal'] = DatetimeLocalColumn
SUPPORTED_COLUMN_TYPES_MAPPING['File'] = FileColumn
SUPPORTED_COLUMN_TYPES_MAPPING['Email'] = EmailColumn
SUPPORTED_COLUMN_TYPES_MAPPING['Color'] = ColorColumn
SUPPORTED_COLUMN_TYPES_MAPPING['Password'] = PasswordColumn
SUPPORTED_COLUMN_TYPES_MAPPING['Range'] = RangeColumn
SUPPORTED_COLUMN_TYPES_MAPPING['Month'] = MonthColumn
SUPPORTED_COLUMN_TYPES_MAPPING['Search'] = SearchColumn
SUPPORTED_COLUMN_TYPES_MAPPING['Time'] = TimeColumn
SUPPORTED_COLUMN_TYPES_MAPPING['URL'] = UrlColumn
SUPPORTED_COLUMN_TYPES_MAPPING['Week'] = WeekColumn
if HAS_LINES_COLUMN:
    SUPPORTED_COLUMN_TYPES_MAPPING['Select'] = SelectColumn
    SUPPORTED_COLUMN_TYPES_MAPPING['SelectVocabulary'] = SelectColumn
    SUPPORTED_COLUMN_TYPES_MAPPING['DynamicVocabulary'] = SelectColumn
