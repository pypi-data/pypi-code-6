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
    ABUSE_EMAIL = "abuseemail"
    ARTIFACT = "artifact"
    ASN = "asn"
    ASNIP = "asnip"
    AS_CC = "asncc"
    AS_CIDR = "ascidr"
    AS_NAME = "asname"
    AS_UPDATE_DATE = "asupdatedate"
    CIDR = "cidr"
    COUNTRY_CODE = "cc"
    DOMAIN = "domain"
    GEOIP = "geoip"
    HOSTNAME = "hostname"
    HTTP_STATUS = "httpstatus"
    HTTP_REDIR = "httpredir"
    HTTP_HEADERS = "httpheaders"
    IP = "ip"
    IPSET = "ipset"
    LAT = "lat"
    LONG = "long"
    NET_CC = "netcc"
    NET_CIDR = "netcidr"
    NET_DESC = "netdesc"
    NET_NAME = "netname"
    NET_UPDATE_DATE = "netupdatedate"
    PATH = "path"
    PHYSICAL_ADDRESS = "phyaddr"
    SCREENSHOT = "screenshot"
    SPIDER = "spider"
    URL = "url"
    WHOIS = "whois"
    WHOIS_RAW = "raw"

    SEEDED_TASK = "seeded"

    TASKRESULTS = "tmoids"

    TRS_META = "_trs"
    TRS_META_JOB_ID = "jid"
    TRS_META_TARGET_ID = "tid"

    META = "_"
    META_AGENT_NAME = "agent"
    META_START_TIME = "stime"
    META_END_TIME = "etime"
    META_SUCCESS = "ok"
    META_RESULT = "r"
    META_TASK_NAME = "tname"
    META_TASK_VERSION = "v"
    META_ERR = "e"
    META_MSG = "m"

    TASKS_ASNIP = "asnip_task"
    TASKS_GEOIP = "geoip_task"
    TASKS_HTTP_STATUS = "http_status_task"
    TASKS_RESOLVER = "resolver_task"
    TASKS_WHOIS = "whois_task"


class MsgValues(ConstantDict):
    HTTP_STATUS_NONCONNECT = -1


class MsgErrs(ConstantDict):
    INPUT_INCORRECT_FORMAT = "INPUT_INCORRECT_FORMAT::{0}"
    INPUT_MISSING = "INPUT_MISSING::{0}"

    HOSTNAME_UNRESOLVABLE = "HOSTNAME_UNRESOLVABLE::{0}"
    HOSTNAME_INVALID = "HOSTNAME_INVALID::{0}"

    LOOKUP_FAILED = "LOOKUP_FAILED::{0}"

    RESULT_FAIL = "TASK_RESULT_FAIL::{0}"
    RESULT_INVALID = "RESULT_INVALID::{0}"

    UNSPECIFIED_ERROR = "UNSPECIFIED_ERROR::{0}"

    URL_INVALID = "URL_INVALID::{0}"
    URL_TIMEOUT = "URL_TIMEOUT::{0}"
    URL_CONN_ERROR = "URL_CONN_ERROR::{0}"
