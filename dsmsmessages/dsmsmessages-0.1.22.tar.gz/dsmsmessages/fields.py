# -*- coding: utf-8 -*-

# ConstantDict as detailed at
# http://loose-bits.com/2011/06/constantdict-yet-another-python.html


class ConstantDict(object):
    """An enumeration class."""
    _dict = None

    @classmethod
    def dict(cls):
        """Dictionary of all upper-case constants."""
        if cls._dict is None:
            val = lambda x: getattr(cls, x)
            cls._dict = dict(((c, val(c)) for c in dir(cls)
                             if c == c.upper()))
        return cls._dict

    def __contains__(self, value):
        return value in self.dict().values()

    def __iter__(self):
        for value in self.dict().values():
            yield value

    def __getattr__(self, name):
        if name in self.dict():
            return self._dict[name]
        else:
            return object.__getattribute__(self, name)


class MsgFields(ConstantDict):
    ASNIP = "asnip"
    ARTIFACT = "artifact"
    COUNTRY_CODE = "cc"
    LAT = "lat"
    LONG = "long"
    DOMAIN = "domain"
    GEOIP = "geoip"
    HOSTNAME = "hostname"
    HTTP_STATUS = "httpstatus"
    IP = "ip"
    IPSET = "ipset"
    PATH = "path"
    SCREENSHOT = "screenshot"
    SPIDER = "spider"
    URL = "url"
    WHOIS = "whois"
    WHOIS_RAW = "raw"

    TASKRESULTS = "tmoids"

    TRS_META = "_trs"
    TRS_META_JOB_ID = "jid"
    TRS_META_TARGET_ID = "tid"

    META = "_"
    META_START_TIME = "stime"
    META_END_TIME = "etime"
    META_SUCCESS = "ok"
    META_RESULT = "r"
    META_VERSION = "v"
    META_ERR = "e"
    META_MSG = "m"


class MsgErrs(ConstantDict):
    INPUT_INCORRECT_FORMAT = "INPUT_INCORRECT_FORMAT::{0}"
    INPUT_MISSING = "INPUT_MISSING::{0}"

    HOSTNAME_UNRESOLVABLE = "HOSTNAME_UNRESOLVABLE::{0}"
    HOSTNAME_INVALID = "HOSTNAME_INVALID::{0}"

    RESULT_INVALID = "RESULT_INVALID::{0}"

    UNSPECIFIED_ERROR = "UNSPECIFIED_ERROR::{0}"

    URL_INVALID = "URL_INVALID::{0}"
    URL_TIMEOUT = "URL_TIMEOUT::{0}"
    URL_CONN_ERROR = "URL_CONN_ERROR::{0}"
