#coding: utf-8

from m3.db import BaseEnumerate

from simple_report.report import FileConverter


class ReportType(BaseEnumerate):
    """
    Тип хранимого отчета
    """
    DOCUMENT = 1
    TABLE = 2

    values = {
        DOCUMENT: u"Документ",
        TABLE: u"Электронная таблица"
    }

    @classmethod
    def get_type(cls, file_extension):
        """
        Отдает соответствующий тип по расширению файла
        """
        if file_extension in ('doc','docx','odf', 'odt'):
            return cls.DOCUMENT
        elif file_extension in ('xls', 'xlsx','ods'):
            return cls.TABLE
        else:
            return None

    @classmethod
    def get_enum(cls, type):
        """
        Отдает соответствующее типу перечисление

        :param type: Тип хранимого отчета
        """
        if type == cls.DOCUMENT:
            return DocumentResultFileTypes
        elif type == cls.TABLE:
            return TableDocumentResultFileTypes
        else:
            return None


class DocumentResultFileTypes(BaseEnumerate):
    """
    Перечисление типов текстовых документов
    """
    PDF = 1
    DOC = 2
    DOCX = 3
    RTF = 4
    ODT = 5
    HTML = 6

    values = {
        PDF: dict(type=FileConverter.PDF, extension='pdf'),
        DOC: dict(type=FileConverter.DOC, extension='doc'),
        DOCX: dict(type=FileConverter.DOCX, extension='docx'),
        RTF: dict(type=FileConverter.RTF, extension='rtf'),
        ODT: dict(type=FileConverter.ODT, extension='odt'),
        HTML: dict(type=FileConverter.HTML, extension='html')
    }

    type_info = {
        PDF: u'Документ PDF (*.pdf)',
        DOC: u'Office 97-2003 (*.doc)',
        DOCX: u'Office 2007-2010 (*.docx)',
        RTF: u'Документ RTF (*.rtf)',
        ODT: u'OpenOffice (*.odt)',
        HTML: u'HTML-страница (*.html)'
    }

    @classmethod
    def default(cls):
        return cls.DOCX


class TableDocumentResultFileTypes(BaseEnumerate):
    """
    Перечисление типов электронных таблиц
    """
    PDF = 1
    XLS = 2
    XLSX = 3
    ODS = 4
    HTML = 5

    values = {
        PDF: dict(type=FileConverter.PDF, extension='pdf'),
        XLS: dict(type=FileConverter.XLS, extension='xls'),
        XLSX: dict(type=FileConverter.XLSX, extension='xlsx'),
        ODS: dict(type=FileConverter.ODS, extension='ods'),
        HTML: dict(type=FileConverter.HTML, extension='html')
    }

    type_info = {
        PDF: u'Документ PDF (*.pdf)',
        XLS: u'Office 97-2003 (*.xls)',
        XLSX: u'Office 2007-2010 (*.xlsx)',
        ODS: u'OpenOffice (*.ods)',
        HTML: u'HTML-страница (*.html)'
    }

    @classmethod
    def default(cls):
        return cls.XLSX


class MimeTypes(BaseEnumerate):

    XLSX = 'xlsx'
    ODS = 'ods'
    DOCX = 'docx'
    PDF = 'pdf'
    HTML = 'html'
    DOC = 'doc'
    XLS = 'xls'
    ODT = 'odt'
    RTF = 'rtf'

    values = {
        XLSX: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        XLS: "application/vnd.ms-excel",
        DOCX: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        DOC: "application/msword",
        ODS: "application/vnd.oasis.opendocument.spreadsheet, application/x-vnd.oasis.opendocument.spreadsheet",
        ODT: "application/vnd.oasis.opendocument.text, application/x-vnd.oasis.opendocument.text",
        PDF: "application/pdf",
        HTML: "text/html",
        RTF: "application/rtf"
    }