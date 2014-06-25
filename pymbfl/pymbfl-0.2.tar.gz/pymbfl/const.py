#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pymbfl public constants"""


__author__ = "Dmitry Selyutin"
__license__ = "GNU LGPL"
__maintainer__ = "Dmitry Selyutin"
__email__ = "ghostmansd@solidlab.ru"


import core


FLAG_SBCS       = 0x00000001
FLAG_MBCS       = 0x00000002
FLAG_WCS2BE     = 0x00000010
FLAG_WCS2LE     = 0x00000020
FLAG_MWC2BE     = 0x00000040
FLAG_MWC2LE     = 0x00000080
FLAG_WCS4BE     = 0x00000100
FLAG_WCS4LE     = 0x00000200
FLAG_MWC4BE     = 0x00000400
FLAG_MWC4LE     = 0x00000800
FLAG_SHIFT      = 0x00001000
FLAG_STRM       = 0x00002000
FLAG_UNSAFE     = 0x00004000


ENCODINGS = (
    "UTF-8", "BASE64", "Quoted-Printable", "UTF-32", "UTF-32BE", "UTF-32LE",
    "UTF-16", "UTF-16BE", "UTF-16LE", "UTF-7", "EUC-JP", "SJIS", "CP932",
    "ISO-2022-JP", "ISO-2022-JP-2004", "GB18030", "EUC-CN", "CP936", "BIG-5",
    "CP950", "EUC-KR", "ISO-2022-KR", "HZ",
    # The last two are not determined
    "SJIS-2004", "UHC",
)
