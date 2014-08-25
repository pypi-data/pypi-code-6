from os import path as opath

from blazeutils.testing import assert_equal_txt
from sqlalchemybwc.lib.testing import query_to_str

cdir = opath.dirname(__file__)

def eq_html(html, filename):
    with open(opath.join(cdir, 'data', filename), 'rb') as fh:
        file_html = fh.read()
    assert_equal_txt(html, file_html)

def assert_in_query(obj, test_for):
    if hasattr(obj, 'build_query'):
        query = obj.build_query()
    else:
        query = obj
    query_str = query_to_str(query)
    assert test_for in query_str, query_str

def assert_not_in_query(obj, test_for):
    if hasattr(obj, 'build_query'):
        query = obj.build_query()
    else:
        query = obj
    query_str = query_to_str(query)
    assert test_for not in query_str, query_str
