#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
"""
Note:
    All sizes used in this module should be in millimeters.

API
---
"""
# Imports =====================================================================
from pyPdf import PdfFileWriter, PdfFileReader
from pyPdf.generic import FloatObject


# Variables ===================================================================
POINT_MM = 25.4 / 72.0  #: 1pt = inch/72, 1 inch = 25.4 mm


# Functions & objects =========================================================
def get_width_height(page):
    """
    Return width and height of the `page`.

    Args:
        page (obj): ``PdfFileReader.pages`` instance.

    Returns:
        tuple: ``(width, height)`` as float, in millimeters.
    """
    return (
        float(page.mediaBox.getWidth()) * POINT_MM,
        float(page.mediaBox.getHeight()) * POINT_MM
    )


def crop_page(page, left, right, top, bottom):
    """
    Crop `page` to size given by `left`, `right`, `top` and `bottom`.

    Args:
        page (obj): :mod:`pyPdf` PdfFileReader's page object.
        left (int): Cut X millimeters from left.
        right (int): Cut X millimeters from right.
        top (int): Cut X millimeters from top.
        bottom (int): Cut X millimeters from bottom.

    Warning:
        This functions modifies the `page` reference!

    Returns:
        obj: Modified page object.
    """
    page.mediaBox.upperRight = (
        page.mediaBox.getUpperRight_x() - FloatObject(right / POINT_MM),
        page.mediaBox.getUpperRight_y() - FloatObject(top / POINT_MM)
    )
    page.mediaBox.lowerLeft = (
        page.mediaBox.getLowerLeft_x() + FloatObject(left / POINT_MM),
        page.mediaBox.getLowerLeft_y() + FloatObject(bottom / POINT_MM)
    )

    return page


def crop_all(pdf, left, right, top, bottom, remove=[]):
    """
    Crop all pages in `pdf`. Remove pages specified by `remove`.

    Args:
        pdf (obj): :mod:`pyPdf` :class:`PdfFileReader` object.
        left (int): Cut X millimeters from left.
        right (int): Cut X millimeters from right.
        top (int): Cut X millimeters from top.
        bottom (int): Cut X millimeters from bottom.
        remove (list/tuple, default []): List of integers. As the function
               iterates thru the pages in `pdf`, indexes of the pages which
               matchs those in `remove` will be skipped.

    Returns:
        obj: :class:`PdfFileWriter` instance, with modified pages.
    """
    out = PdfFileWriter()

    # crop pages
    for cnt, page in enumerate(pdf.pages):
        if cnt in remove:
            continue

        out.addPage(
            crop_page(page, left, right, top, bottom)
        )

    return out


def crop_differently(pdf, even_vector, odd_vector, remove=[]):
    """
    Crop `pdf` even pages by `even_vector` and odd pages by `odd_vector`.
    Remove pages specified by `remove`.

    Args:
        pdf (obj): :mod:`pyPdf` :class:`PdfFileReader` object.
        even_vector (list): List of coordinates to which all even pages will
                    be cropped. ``[Left, Right, Top, Bottom]``.
        edd_vector (list): List of coordinates to which all odd pages will
                    be cropped. ``[Left, Right, Top, Bottom]``.
        remove (list/tuple, default []): List of integers. As the function
               iterates thru the pages in `pdf`, indexes of the pages which
               matchs those in `remove` will be skipped.

    Returns:
        obj: :class:`PdfFileWriter` instance, with modified pages.
    """
    out = PdfFileWriter()

    # crop pages
    for cnt, page in enumerate(pdf.pages):
        if cnt in remove:
            continue

        crop_vector = even_vector if (cnt % 2) == 0 else odd_vector
        out.addPage(
            crop_page(page, *crop_vector)
        )

    return out


def remove_pages(pdf, remove):
    """
    Remove pages specified in vector `remove`.

    Args:
        pdf (obj): :mod:`pyPdf` :class:`PdfFileReader` object.
        remove (list/tuple, default []): List of integers. As the function
               iterates thru the pages in `pdf`, indexes of the pages which
               matchs those in `remove` will be skipped.

    Returns:
        obj: :class:`PdfFileWriter` instance, with modified pages.
    """
    out = PdfFileWriter()

    # crop pages
    for cnt, page in enumerate(pdf.pages):
        if cnt in remove:
            continue

        out.addPage(page)

    return out


def read_pdf(filename):
    """
    Read pdf file specified by `filename`.

    Args:
        filename (str): Path to the pdf file.

    Returns:
        obj: :class:`PdfFileReader` object.
    """
    return PdfFileReader(
        open(filename, 'rb')
    )


def save_pdf(filename, content):
    """
    Save `content` to `filename`.

    Args:
        filename (str): Path which will be used for `content`.
        content (obj): :class:`PdfFileWriter` object which will be serialized.
    """
    with file(filename, 'wb') as f:
        content.write(f)
