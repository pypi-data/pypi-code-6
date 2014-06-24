# -*- coding: utf-8 -*-
# Copyright (c) 2011-2014 Polyconseil SAS. All rights reserved.f

from __future__ import unicode_literals

import logging
from StringIO import StringIO

from dokang.harvesters import Harvester

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument    
from pdfminer.pdftypes import PDFObjRef


logger = logging.getLogger('dokang')

def extract_content(fp, encoding):
    # Code has been taken from the pdf2txt tool included in PDFMiner.
    # I don't know what I am doing...
    content = StringIO()
    rsrcmgr = PDFResourceManager(caching=True)
    device = TextConverter(
        rsrcmgr, content, codec=encoding, laparams=LAParams(), imagewriter=None)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    device.close()
    content.seek(0)
    return content.getvalue()


class PdfHarvester(Harvester):
    """Harvest content from a PDF."""

    def harvest_file(self, path):
        with open(path) as fp:
            # FIXME: how do we know which encoding to use? Should we
            # use 'chardet' to detect it?
            encoding = 'utf-8'
            parser = PDFParser(fp)
            doc = PDFDocument(parser)
            title = doc.info[0].get('Title', '')
            if isinstance(title, PDFObjRef):
                title = title.resolve()
            try:
                title = title.decode(encoding)
            except UnicodeDecodeError:
                logger.warning('Could not correctly decode title of "%s".', path)
                title = title.decode(encoding, 'ignore')
            content = extract_content(fp, encoding).strip()
            try:
                content = content.decode(encoding)
            except UnicodeDecodeError:
                logger.warning('Could not correctly decode content of "%s".', path)
                content = content.decode(encoding, 'ignore')
        return {
            'title': title,
            'content': content,
            'kind': 'PDF',
        }
