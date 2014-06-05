import csv
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

def colnames(fp, *args, **kwargs):
    pos = fp.tell()
    result = next(csv.reader(fp, *args, **kwargs))
    fp.seek(pos)
    return result
