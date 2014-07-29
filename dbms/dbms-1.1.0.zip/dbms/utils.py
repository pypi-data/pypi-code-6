"""
Utilities to work with cursors and write queries independent of 
server implementations.

"""

import json as _json
import sys as _sys
from datetime import date as _date
from . import cursors as _cursors

_warnings = None

class Param(object):
    """Parameter to use with formatQuery()"""
    def __init__(self, value):
        self.value = value
        
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.value)
    
class NamedParam(Param):
    """Named parameter to use with formatQuery()"""
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def __repr__(self):
        return '%s(%s, %r)' % (self.__class__.__name__, self.name, self.value)
    
def formatQuery(chunks, paramstyle):
    """
    Return formatted query and parameter list 
    
    chunks is an array of query pieces that are either text or instance of Param class.
    Usage:
    query = ('SELECT * FROM people WHERE status = ', 
            Param('A'), 
            ' AND last_name LIKE ',
            NamedParam('last_name', 'Smith%'), 
            ' ORDER BY last_name, first_name') 
    sql, params = formatQuery(query, 'named')   
    Adapted from: http://code.activestate.com/recipes/278612-single-parameters-style-for-db-api-modules/
    """
    dictParamStyles = ('named', 'pyformat')
    queryParts = []
    if paramstyle in dictParamStyles:
        params = {}
    else:
        params = []
        
    placeholders = {'named': ':%s',
                    'pyformat': '%%(%s)s',
                    'format': '%s',
                    'qmark': '?',
                    'numeric': ':%d'}
    
    if paramstyle not in placeholders:
        raise ValueError("%s not a valid paramstyle" % paramstyle)
    
    for chunk in chunks:
        if isinstance(chunk, Param):
            if paramstyle in dictParamStyles:
                if hasattr(chunk, 'name'):
                    name = chunk.name
                else:
                    name = 'p%d' % (len(params) + 1)
                params[name] = chunk.value
                queryParts.append(placeholders[paramstyle] % name)
            else:
                params.append(chunk.value)
                if paramstyle == 'numeric':
                    queryParts.append(':%d' % len(params))
                else:
                    queryParts.append(placeholders[paramstyle])
        else:
            queryParts.append(chunk)
    return (' '.join(queryParts), params)                 

def _toString(obj):
    ret = ''
    if obj is None:
        ret = '(NULL)'
    elif isinstance(obj, _date):
        # datetime.datetime is subclassed from date
        if hasattr(obj, 'microsecond') and obj.microsecond:
            ret = _date.strftime(obj, '%Y-%m-%d %H:%M:%S.%f %Z')
        elif hasattr(obj, 'hour') and (obj.hour or obj.minute or obj.second):
            ret = _date.strftime(obj, '%Y-%m-%d %H:%M:%S')
        else:
            ret = _date.strftime(obj, '%Y-%m-%d')
    else:
        ret = str(obj)
    return ret

def _fixedWidth(value, width):
    """Convert value to string and trim or pad as needed"""
    global _warnings
    ret = _toString(value)
    if len(ret) > width:
        if not _warnings:
            _warnings = 'WARNING - Some values were truncated during export.'
        return ret[0:width]
    return ret.ljust(width)

class _JSONEncoder(_json.JSONEncoder):
    """ JSONEncoder that handles dates."""
    def default(self, obj):
        if isinstance(obj, _date):
            encoded_obj = _toString(obj)
        elif isinstance(obj, _cursors.Record):
            encoded_obj = super(_JSONEncoder, self).default(obj.copy())
        elif hasattr(obj, '_asdict'):
            encoded_obj = super(_JSONEncoder, self).default(obj._asdict())
        else:
            encoded_obj = super(_JSONEncoder, self).default(obj)
        return encoded_obj

def createInsert(cur, table, paramstyle=None):
    """Create Insert Statement"""
    if not paramstyle:
        paramstyle = cur.connection.interface.paramstyle
    cur.execute('SELECT * FROM %s WHERE 0=1' % table)
    columns = cur.columns()
    
    if paramstyle == 'qmark':
        params = ', '.join(['?' for c in columns])
    elif paramstyle == 'numeric':
        params = ', '.join([':%d' % (i+1) for i in range(len(columns))])
    elif paramstyle == 'format':
        params = ', '.join(['%s' for c in columns])
    elif paramstyle == 'named':
        params = ', '.join([':%s' % c for c in columns])
    elif paramstyle == 'pyformat':
        params = ', '.join(['%%(%s)s' % c for c in columns])
    
    query = 'INSERT INTO %s\n(%s)\nVALUES(%s)' % (table,
                                                  ', '.join(columns),
                                                  params)
    return query

    
def cursorToCursorCopy(src, dest, destTable):
    """
    Copy record set from source to destination cursor. 
    This can be used to copy data across different servers. However, their
    data types need to be similar.
    
    This does not perform constraint checks and will fail if you try to 
    insert a record that already exists on the destination table. 
    """
    query = createInsert(dest, destTable)
    inserts = 0
    
    rows = src.fetchmany()
    while rows:
        dest.executemany(query, rows)
        inserts += len(rows) 
        rows = src.fetchmany()
    print('Inserted %d records into %s' % (inserts, destTable))
    
def cursorToCSV(cur, filename):
    """Exports cursor to CSV file"""
    import csv
    if _sys.version_info >= (3,0,0):
        dest = csv.writer(open(filename, 'w', newline=''))
    else:
        dest = csv.writer(open(filename, 'wb'))
    dest.writerow(cur.columns(cur.UPPER_CASE))
    for rec in cur:
        dest.writerow([_toString(val) for val in rec])

def cursorToFixedWidth(cur, filename=None, colWidths=()):
    """
    Exports cursor to fixed width text.
    If colWidths are passed in values will be truncated if they exceed that.
    If colWidths are not passed, they will be calculated based on the first
    20 rows and values will not be truncated.
    """
    global _warnings
    if filename:
        # print to file if filename given
        fp = open(filename, 'w')
    else:
        # else print to stdout
        fp = _sys.stdout
        
    cols = cur.columns()
    if not colWidths:
        # column widths were not passed in. Calculate based on the first 20 rows    
        colWidths = []
        trimToWidth = False
        
        for col in cols:
            colWidths.append(len(col))
        #sample column widths of first 20 records
        rows = cur.fetchmany(20)
        for row in rows:
            for i in range(len(cols)):
                strLen = len(_toString(row[i]))
                if strLen > colWidths[i]:
                    colWidths[i] = strLen
        # pad a bit
        for i in range(len(cols)):
            colWidths[i] = 2 + int(colWidths[i] * 1.1)
    
        #write column headers
        fp.write('%s\n' % ''.join([cols[i].upper().ljust(colWidths[i]) for i in range(len(cols))]))
    else:
        # column widths were passed in 
        if len(colWidths) != len(cols):
            raise Exception('Length of colWidths parameter must match number of columns.')
        trimToWidth = True
        rows = cur.fetchmany(20)
    while rows:
        for row in rows:
            if trimToWidth:
                fp.write('%s\n' % ''.join([_fixedWidth(row[i], colWidths[i]) for i in range(len(cols))]))
            else:
                fp.write('%s\n' % ''.join([_toString(row[i]).ljust(colWidths[i]) for i in range(len(cols))]))
        rows = cur.fetchmany(20)
        
    if filename:
        fp.close()
        
    if _warnings:
        print(_warnings)
        _warnings = None

def cursorToXLSX(cur, filename, exportQuery=True):
    """Exports cursor to Excel file. Requires xlswriter."""
    import xlsxwriter
    wb = xlsxwriter.Workbook(filename)
    ws = wb.add_worksheet('Data')
    bold_fmt = wb.add_format({'bold': True})
    date_fmt = wb.add_format({'num_format': 'yyyy-mm-dd'})
    ws.write_row(0, 0, cur.columns(cur.UPPER_CASE), bold_fmt)
    row = 1
    for rec in cur:
        ws.write_row(row, 0, rec)
        row += 1
    for i in range(len(rec)):
        val_len = len(str(rec[i]))
        if isinstance(rec[i], _date):
            ws.set_column(i, i, 15, date_fmt)
        elif val_len > 20:
            ws.set_column(i, i, round(val_len * 1.25))
        else:
            ws.set_column(i, i, 12)
            
    if exportQuery:
        # export query to a second worksheet
        wrap = wb.add_format()
        wrap.set_text_wrap(1)
        wrap.set_valign('top')
        qws = wb.add_worksheet('Query')
        qws.write(0, 0, cur.showStatement(), wrap)
        qws.set_column(0, 0, 80)
        qws.set_row(0, 300)

    wb.close()
        
def cursorToXML(cur, filename, prettyprint=True, exportQuery=True):
    """Exports cursor to XML file"""
    try:
        from lxml import etree as et
    except ImportError:
        import xml.etree.ElementTree as et
    
    fp = open(filename, 'wb') 
    root = et.Element("root")
    if exportQuery:
        root.append(et.Comment("\nQuery:\n%s" % cur.showStatement()))
    cols = cur.columns()
    rn = 0
    for rec in cur:
        rn += 1
        row = et.SubElement(root, 'row', {'num': str(rn)})
        for col in cols:
            if rec[col]:
                et.SubElement(row, col).text = str(rec[col])
                
    fp.write(et.tostring(root, pretty_print = prettyprint))
 
def cursorToJSON(cur, filename=None):
    """Export cursor to JSON encoded string"""
    if filename:
        # print to file if filename given
        fp = open(filename, 'w')
    else:
        # else print to stdout
        fp = _sys.stdout
    fp.write('[')
    # Must be converted to dict in order to encode properly
    if isinstance(cur, _cursors.DictCursor):
        toDict = lambda r: r.copy()
    elif isinstance(cur, _cursors.NamedTupleCursor):
        toDict = lambda r: r._asdict()
    else:
        toDict = lambda r: dict(zip(cur.columns, r))
        
    for rec in cur:
        fp.write('\n%s,' % _json.dumps(toDict(rec), cls=_JSONEncoder))
    fp.write('\n]')