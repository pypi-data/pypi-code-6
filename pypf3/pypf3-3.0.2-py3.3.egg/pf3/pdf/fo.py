import logging
import traceback

COMMASPACE = ', '

class fo():

    obj = {}
    pages = []

    defaultFont = {
        'family': 'Times Roman',
        'size': "12pt"
    }


    def __init__(self):
        self.logger = logging.getLogger('pf3')
        # assume at least one page
        self.addPage(1)

    def addPage(self, page_number, page):
        # page numbers start at 1

        # if in between pages not there, put them in now
        if (len(self.pages) < page_number):
            p = len(self.pages)
            while (p < page_number-1):
               self.pages[p]  = {}
               p += 1

        self.pages[page_number] = page

    def addPageElement(self, page_number, element):
        page = self.getPage(page_number)
        self.pages['page_number']['elements'].append(element)


    def getPage(self, page_number):
        # page numbers start at 1
        return self.pages[page_number - 1]

    def toXml(self):
        result = '<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format" font-family="'+self.defaultFont['family']+" font-size="+self.defaultFont['family']+'">'
        result += '<fo:layout-master-set>'
        result += '<fo:page-sequence>'
        result += '</fo:page-sequence>'
        result += '</fo:layout-master-set>'
        result += '</fo:root>'
        return result;


