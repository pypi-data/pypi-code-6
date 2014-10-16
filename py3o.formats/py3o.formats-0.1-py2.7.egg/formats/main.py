# -*- coding: utf-8 -*-

DEFAULT_MIMETYPE = "application/octet-stream"

FORMAT_WORD97 = "doc"
FORMAT_WORD2003 = "docx"
FORMAT_PDF = "pdf"
FORMAT_DOCBOOK = "docbook"
FORMAT_HTML = "html"
FORMAT_ODT = "odt"


class UnkownFormatException(Exception):
    pass


class Format(object):

    def __init__(self, name, odfname, mimetype=DEFAULT_MIMETYPE):
        self.name = name
        self.odfname = odfname
        self.mimetype = mimetype


class Formats(object):

    def __init__(self):

        self._formats = {
            FORMAT_WORD97: Format(
                FORMAT_WORD97, "MS Word 97", "application/msword"
            ),
            FORMAT_WORD2003: Format(
                FORMAT_WORD2003, "MS Word 2003 XML",
                "application/vnd.openxmlformats-officedocument"
                ".wordprocessingml.document"
            ),
            FORMAT_PDF: Format(
                FORMAT_PDF, "writer_pdf_Export", "application/pdf"
            ),
            FORMAT_DOCBOOK: Format(
                FORMAT_DOCBOOK, "DocBook File", "application/xml"
            ),
            FORMAT_HTML: Format(FORMAT_HTML, "HTML", "text/html"),
            FORMAT_ODT: Format(
                FORMAT_ODT, "application/vnd.oasis.opendocument.text"
            ),
        }

    def get_format(self, name):
        f = self._formats.get(name)

        if not f:
            raise UnkownFormatException("Format {} is unkown".format(name))

        return f

    def get_known_format_names(self):
        return [f for f in self._formats]
