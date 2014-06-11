import os
from util import *

class LogParser(object):
    """Abstract class for log parsers for specific formats.
    Subclasses must override parse() to return a list of rows
    with column headings as keys.
    """
    def __init__(self):
        super(LogParser, self).__init__()

    @classmethod
    def parse_file(cls, file_path, format_hint=None):
        # choose a subclass based on extension or hint
        subs = [TDF_LogParser, CSV_LogParser, FIDL_LogParser]
        parser = None
        if format_hint != None:
            ext = format_hint
        else:
            ext = os.path.splitext(file_path)[-1]
        for sub in subs:
            if ext in sub.supported_exts():
                parser = sub
                break
        if parser == None:
            raise ValueError("Could not find valid parser for %s" % file_path)
        parser = parser()
        return parser.parse(file_path)

    """ Override in subclasses """
    @classmethod
    def supported_exts(cls):
        return NotImplementedError()
    def parse(self, file_path):
        return NotImplementedError()

class TDF_LogParser(LogParser):
    """A parser that reads tab delimited files"""
    @classmethod
    def supported_exts(self):
        return ['.txt','.tdf']
    
    def parse(self, file_path):
        return read_tdf(file_path)

class CSV_LogParser(LogParser):
    """A parser that reads csv files"""
    @classmethod
    def supported_exts(self):
        return ['.csv',]
    
    def parse(self, file_path):
        return read_csv(file_path)

class FIDL_LogParser(LogParser):
    """A parser that reads FIDL files"""
    @classmethod
    def supported_exts(self):
        return ['.fidl',]
    
    def parse(self, file_path):
        from math import floor
        header = None
        lines = []
        with open(file_path, 'r') as f:
            for line in f:
                sline = line.strip()
                if not sline:
                    continue
                if not header:
                    header = sline
                    continue
                lines.append(sline)
        header = header.split()
        tr = float(header[0])
        conds = {}
        for i, h in enumerate(header[1:]):
            hs = h.split("_")
            if len(hs) > 1:
                hs = hs[1:] if hs[0].isdigit() else hs
            conds[i] = "_".join(hs)
        events = []
        for line in lines:
            words = line.split()
            if len(words) < 3:
                continue
            try:
                onset = float(words[0])
                name = conds.get(int(words[1]), None)
                duration = float(words[2])
                tr_idx = int(floor(onset / tr))
            except Exception, e:
                continue
            events.append({"name":name,"onset":onset,"duration":duration,"tr_idx":tr_idx})
        return events

