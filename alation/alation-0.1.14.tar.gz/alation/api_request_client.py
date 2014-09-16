import os
import re

try:
    from io import StringIO as StringIO
except ImportError:
    import StringIO

try:
    import urllib.request as urllib2
except:
    import urllib2


class AlationError(Exception):
    pass


def convert_to_string(bytes_or_string):
    try:
        return bytes_or_string.decode(encoding='UTF-8')
    except AttributeError:
        return bytes_or_string


def handle_exception(code):
    if code == 404:
        raise AlationError(
            "404: Your base url may be wrong, or the query with that id may not exist")
    elif code == 403:
        raise AlationError(
            "403: Permission denied. If this is incorrect, try regenerating your API token")
    else:
        raise AlationError("HTTP Error: " + str(code))


def read_config_file():
    try:
        home = os.path.expanduser('~')
        f = open(home + "/.alation_api_config", "r")
        token = f.readline().rstrip()
        base_url = f.readline().rstrip()
        return (token, base_url)
    except IOError:
        raise AlationError(
            "Can't find your alation_api_config file. Please run alation-setup")


def make_request(request_id, request_type, response_type):
    (token, base_url) = read_config_file()
    request_url = "/api/" + request_type + \
        "/" + str(request_id) + "/" + response_type + "/"
    request = urllib2.Request(base_url + request_url)
    request.add_header("token", token)
    return request


def get_sql(qid):
    """Returns SQL of a query based on its unique query id.
    """
    request = make_request(qid, "query", "sql")
    try:
        response = urllib2.urlopen(request)
        # probably won't actually be used, but just in case
        code = response.getcode()
        if code != 200:
            handle_exception(code)
        return convert_to_string(response.read())
    except urllib2.HTTPError as error:
        handle_exception(error.code)


def get_result(rid):
    """Returns CSV of a particular ExecutionResult from its unique id.
    """
    request = make_request(rid, "result", "csv")
    try:
        response = urllib2.urlopen(request)
        output = StringIO.StringIO()
        CHUNK = 16 * 1024
        while True:
            chunk = response.read(CHUNK)
            if not chunk:
                break
            output.write(chunk)
        return output.getvalue()
    except urllib2.HTTPError as error:
        handle_exception(error.code)


def subbed_query(qid, replacements):
    sql = get_sql(qid)
    for key in replacements:
        sql = re.sub(u"\$\{" + key + "\}", replacements[key], sql)
    return sql
