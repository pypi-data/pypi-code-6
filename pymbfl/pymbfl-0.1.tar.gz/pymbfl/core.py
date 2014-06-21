#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""pymbfl public API"""


__author__ = "Dmitry Selyutin"
__license__ = "GNU LGPL"
__maintainer__ = "Dmitry Selyutin"
__email__ = "ghostmansd@solidlab.ru"


import ctypes
import locale
import const


#==============================================================================#
# libmbfl and "typedefs" ======================================================#
#==============================================================================#
_c_str = ctypes.c_char_p
_c_int = ctypes.c_int
_c_uint = ctypes.c_uint
_c_ubyte = ctypes.c_ubyte
_c_struct = ctypes.Structure
_c_ubyte_p = ctypes.POINTER(_c_ubyte)
_c_str_p = ctypes.POINTER(_c_str)
try:
    _libmbfl = ctypes.CDLL("libmbfl.so.1")
    _mbfl_no2encoding = _libmbfl.mbfl_no2encoding
    _mbfl_name2encoding = _libmbfl.mbfl_name2encoding
    _mbfl_name2language = _libmbfl.mbfl_name2language
    _mbfl_identify_encoding2 = _libmbfl.mbfl_identify_encoding2
except (OSError, AttributeError) as error:
    raise RuntimeError(error.message)


#==============================================================================#
# struct _mbfl_encoding =======================================================#
#==============================================================================#
class _mbfl_encoding(_c_struct):
    """typedef struct _mbfl_encoding {
        enum enum_encoding no_encoding;
        const char *name;
        const char *mime_name;
        const char *(*aliases)[];
        const unsigned char *mblen_table;
        unsigned int flag;
    } _mbfl_encoding;"""
    _fields_ = [
        ("no_encoding",         _c_int),
        ("name",                _c_str),
        ("mime_name",           _c_str),
        ("aliases",             _c_str_p),
        ("mblen_table",         _c_ubyte_p),
        ("flag",                _c_uint),
    ]

_mbfl_encoding_p = ctypes.POINTER(_mbfl_encoding)


#==============================================================================#
# struct _mbfl_language =======================================================#
#==============================================================================#
class _mbfl_language(_c_struct):
    """typedef struct _mbfl_language {
        enum mbfl_no_language no_language;
        const char *name;
        const char *short_name;
        const char *(*aliases)[];
        enum mbfl_no_encoding mail_charset;
        enum mbfl_no_encoding mail_header_encoding;
        enum mbfl_no_encoding mail_body_encoding;
    } mbfl_language;"""
    _fields_ = [
        ("no_language",                 _c_int),
        ("name",                        _c_str),
        ("short_name",                  _c_str),
        ("aliases",                     _c_str_p),
        ("mail_charset",                _c_int),
        ("mail_header_encoding",        _c_int),
        ("mail_body_encoding",          _c_int),
    ]

_mbfl_language_p = ctypes.POINTER(_mbfl_language)


#==============================================================================#
# struct _mbfl_string =========================================================#
#==============================================================================#
class _mbfl_string(_c_struct):
    """typedef struct _mbfl_string {
        enum mbfl_no_language no_language;
        enum enum_encoding no_encoding;
        unsigned char *val;
        unsigned int len;
    } _mbfl_string;"""
    _fields_ = [
        ("no_language", _c_int),
        ("no_encoding", _c_int),
        ("val",         _c_ubyte_p),
        ("len",         _c_uint),
    ]

_mbfl_string_p = ctypes.POINTER(_mbfl_string)


#==============================================================================#
# C API type check ============================================================#
#==============================================================================#
_mbfl_name2encoding.argtypes = [_c_str]
_mbfl_name2encoding.restype = _mbfl_encoding_p

_mbfl_no2encoding.argtypes = [_c_int]
_mbfl_no2encoding.restype = _mbfl_encoding_p

_mbfl_name2language.argtypes = [_c_str]
_mbfl_name2language.restype = _mbfl_language_p

_mbfl_identify_encoding2.argtypes = [
    _mbfl_string_p, ctypes.POINTER(_mbfl_encoding_p), _c_int, _c_int]
_mbfl_identify_encoding2.restype = _mbfl_encoding_p


#==============================================================================#
# class Language ==============================================================#
#==============================================================================#
class Language(object):
    """Language provides information about libmbfl language type."""

    def __init__(self, name):
        """Create libmbfl language wrapper."""
        if (name == "C" or name == "POSIX"):
            name = "neutral"
        res = _mbfl_name2language(name)
        if not res:
            raise ValueError("unknown language: %s" % repr(name))
        self._struct = res.contents

    def __repr__(self):
        return ("pymbfl.Language(%s)" % repr(self.__str__()))

    def __str__(self):
        return self._struct.short_name

    def __eq__(self, language):
        if isinstance(language, str):
            lhs = self._struct.no_language
            rhs = Language(language)._struct.no_language
        elif isinstance(language, Language):
            lhs = self._struct.no_language
            rhs = language._struct.no_language
        else:
            lhs, rhs = False, True
        return (lhs == rhs)

    @property
    def aliases(self):
        """available aliases for the language"""
        aliases = self._struct.aliases
        if not aliases:
            return list()
        res = []
        index = 0
        alias = None
        for alias in aliases:
            alias = aliases[index]
            if (alias is None):
                break
            res.append(alias)
            index += 1
        return res

    @property
    def short_name(self):
        """short name for the language"""
        return self._struct.short_name

    @property
    def encodings(self):
        """default encodings (mail, header, body)"""
        res = [
            _mbfl_no2encoding(self._struct.mail_charset),
            _mbfl_no2encoding(self._struct.mail_header_encoding),
            _mbfl_no2encoding(self._struct.mail_body_encoding),
        ]
        return [Encoding(i.contents.name) if i else None for i in res]


#==============================================================================#
# class Encoding ==============================================================#
#==============================================================================#
class Encoding(object):
    """Encoding provides information about libmbfl encoding type."""

    def __init__(self, name):
        """Create libmbfl encoding wrapper."""
        name = name.upper()
        res = _mbfl_name2encoding(name)
        if not res:
            raise ValueError("unknown encoding: %s" % repr(name))
        self._struct = res.contents

    def __repr__(self):
        return ("pymbfl.Encoding(%s)" % repr(self.__str__()))

    def __str__(self):
        return str(self._struct.name)

    def __eq__(self, encoding):
        if isinstance(encoding, str):
            lhs = self._struct.no_encoding
            rhs = Encoding(encoding)._struct.no_encoding
        elif isinstance(encoding, Encoding):
            lhs = self._struct.no_encoding
            rhs = encoding._struct.no_encoding
        else:
            lhs, rhs = False, True
        return (lhs == rhs)

    def __ne__(self, encoding):
        return not self.__eq__(encoding)

    @property
    def aliases(self):
        """available aliases for the encoding"""
        aliases = self._struct.aliases
        if not aliases:
            return list()
        res = []
        index = 0
        alias = None
        for alias in aliases:
            alias = aliases[index]
            if (alias is None):
                break
            res.append(alias)
            index += 1
        return ([self.mime] + res)

    @property
    def flags(self):
        """encoding type flags"""
        return self._struct.flag

    @property
    def mime(self):
        """MIME name of the encoding"""
        if self._struct.mime_name:
            return self._struct.mime_name
        return ""


#==============================================================================#
# class Detector ==============================================================#
#==============================================================================#
class Detector(object):
    """Detector object is used to determine encodings for the given text."""

    def __init__(self, language=None, encodings=None):
        """
        Create libmbfl encoding detector.
        If language argument is None, then current locale language will be used
        during determination. If language argument is an empty string, detector
        will language-neutral. Almost the same as in setlocale() function.
        The second argument must be an iterable object, which yields either
        encoding names or Encoding instances. These encodings will be checked
        during determination. If the only argument is omitted, then check
        available multi-byte encodings.
        """
        locale_info = locale.getdefaultlocale()
        if language is None:
            for language in locale_info[0].split('_'):
                language = language.strip()
                if not language:
                    continue
                self.set_language(language)
        elif language != "":
            self.set_language(language)
        else:
            self.set_language("neutral")
        if encodings is None:
            encodings = const.ENCODINGS
        encodings = [i for i in encodings]
        if locale_info[1] not in encodings:
            encodings.append(locale_info[1])
        self.set_encodings(encodings)

    def __repr__(self):
        encodings = str([i.mime for i in self._encodings])[1:-1]
        return ("pymbfl.Detector(%s)" % encodings)

    def get_language(self):
        """Get language which is used during determination."""
        return self._language

    def set_language(self, language):
        """
        Set language which is used during determination.
        Method returns language which was previously used.
        """
        if isinstance(language, Language):
            self._language = language
        if isinstance(language, str):
            res = _mbfl_name2language(language)
            if not res:
                raise ValueError("unsupported language: %s" % repr(language))
            self._language = Language(res.contents.name)
        else:
            raise TypeError("language must be str or Language object")

    def get_encodings(self):
        """Get encodings checked during determination."""
        return self._encodings

    def set_encodings(self, encodings):
        """
        Set encodings checked during determination.
        Method returns encodings which were previously used.
        """
        self._encodings = list()
        for encoding in encodings:
            if isinstance(encoding, str):
                self._encodings.append(Encoding(encoding))
            elif isinstance(encoding, Encoding):
                self._encodings.append(encoding)
            else:
                raise TypeError("each encoding must be str or Encoding object")

    def detect(self, string, strict=True):
        """Determine encoding for the given string."""
        encodings = []
        mbstring = _mbfl_string()
        mbstring.len = len(string)
        mbstring.val = ctypes.cast(string, _c_ubyte_p)
        mbstring.language = self._language._struct.no_language
        for encoding in self._encodings:
            cobject = encoding._struct
            encodings.append( ctypes.pointer(cobject) )
        elistsz = len(encodings)
        elist = (_mbfl_encoding_p * elistsz)(*encodings)
        res = _mbfl_identify_encoding2(
            ctypes.byref(mbstring),
            elist, elistsz, strict)
        if not res:
            return None
        return Encoding(res.contents.name)
