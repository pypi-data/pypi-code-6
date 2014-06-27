import os
import subprocess
import datetime
from unittest import TestCase
from PyODConverter import DocumentConverter, DocumentConversionException

TEST_DATA_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__),
                                               os.path.pardir,
                                               'test_data'))
ODT_FILE_PATH = os.path.join(TEST_DATA_PATH, 'document.odt')
DOCX_FILE_PATH = os.path.join(TEST_DATA_PATH, 'document.docx')
PDF_FILE_PATH = os.path.join(TEST_DATA_PATH, 'document.pdf')
TXT_FILE_PATH = os.path.join(TEST_DATA_PATH, 'document.txt')


class DocumentConverterTest(TestCase):

    def setUp(self):
        self.converter = DocumentConverter(listener=('localhost', 2002))

    def test_fail_connect(self):
        with self.assertRaises(DocumentConversionException):
            DocumentConverter(listener=('localhost', 1337))

    def test_not_existing_document(self):
        with self.assertRaises(DocumentConversionException):
            self.converter.convert("kittens.docx", "docs.pdf")

    def test_convert_docx_to_pdf(self):
        self.converter.convert(DOCX_FILE_PATH, PDF_FILE_PATH)
        self.assertTrue(os.path.exists(PDF_FILE_PATH))

    def test_convert_odt_to_pdf(self):
        self.converter.convert(ODT_FILE_PATH, PDF_FILE_PATH)
        self.assertTrue(os.path.exists(PDF_FILE_PATH))

    def test_fill_data(self):
        self.converter.convert(ODT_FILE_PATH, PDF_FILE_PATH,
                               data={'my_bookmark': 'It rocks !', # bookmark
                                     'my_field': 'Just amazing !', # custom fields
                                     'my_number': 12,
                                     'my_float_number': 0.5,
                                     'my_date': datetime.date(2010, 12, 24),
                                     'Title': "Absolutely fabulous !", # property
                                     'Keywords': ('nice', 'good'),
                                     })

        self.assertTrue(os.path.exists(PDF_FILE_PATH))
        subprocess.call(['pdftotext', PDF_FILE_PATH, TXT_FILE_PATH])
        txt = open(TXT_FILE_PATH).read()
        self.assertIn('It rocks !', txt)
        self.assertIn('Just amazing !', txt)
        self.assertIn('12,00', txt)
        self.assertIn('24.12.2010', txt)
        self.assertIn('Absolutely fabulous', txt)
        self.assertIn('nice, good', txt)
        self.assertIn('0,50', txt)

    def tearDown(self):
        """
        Cleanup
        """
        if os.path.exists(PDF_FILE_PATH):
            os.remove(PDF_FILE_PATH)

        if os.path.exists(TXT_FILE_PATH):
            os.remove(TXT_FILE_PATH)
