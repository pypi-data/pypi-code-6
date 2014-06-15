try:
    import xlwt as xl
except:
    raise Exception("you must download python-xlwt package")
from cStringIO import StringIO

# based on django-excel-templates
ITEM_DATE, ITEM_TIME, ITEM_DATETIME, ITEM_INT, ITEM_FLOAT, ITEM_DECIMAL, \
                                ITEM_UNICODE, ITEM_BOOL, ITEM_HEADER, \
                                ITEM_IMAGE = range(10)

#class Item(object):
#    def __init__(self, val, formatter=None, header=False,force_height=None,force_width=None,
#                 name=""):
#        """
#            val: The value of the item
#            header: bool flag if Item is a header
#        """
#        self.__name = name
#        
#        self.width = force_width
#        self.height = force_height
#
#        self.__val = val
#        
#        try:
#            obtype = type(self.__val)
#        except:
#            obtype = unicode
#        
#        if header == True:
#            self.__type = ITEM_HEADER
#        elif obtype == unicode:
#            self.__type = ITEM_UNICODE
#        elif obtype  == int:
#            self.__type = ITEM_INT
#        elif obtype == bool:
#            self.__type = ITEM_BOOL
#        elif obtype == float:
#            self.set_percision(0 - int(Decimal(str(val)).as_tuple()[2]) )
#            self.__type = ITEM_FLOAT
#        elif obtype == decimal.Decimal:
#            self.set_percision( 0 - int(val.as_tuple()[2]) )
#            self.__type = ITEM_DECIMAL
#        elif obtype == dt.datetime:
#            self.__type = ITEM_DATETIME
#        elif obtype == dt.date:
#            self.__type = ITEM_DATE
#        elif obtype == dt.time:
#            self.__type = ITEM_TIME


class ExcelReport(object):
    def __init__(self, first_sheet_name='Sheet0'):
        self.workbook = xl.Workbook()
        self.workspace = self.workbook.add_sheet(first_sheet_name)
        self.current_row = 0
        super(ExcelReport, self).__init__()


    def add_row(self, values):
        col = 0
        for v in values:
            self.workspace.write(self.current_row, col, v)
            col += 1
        self.current_row += 1


    def write_report(self):
        tfile = StringIO()
        self.workbook.save(tfile)
        tfile.seek(0) # start the file stream from the beginning
        ssheet = tfile.read()
        return ssheet