import api_setup_client as api_setup
import api_request_client as api
from api_request_client import AlationError
import sys


def print_sql(*args):
    try:
        qid = int(sys.argv[1])
        print api.get_sql(qid)
    except ValueError:
        print "Not a valid integer for query id"
    except AlationError, error:
        print error


def print_result(*args):
    try:
        rid = int(sys.argv[1])
        print api.get_result(rid)
    except ValueError:
        print "Not a valid integer for result id"
    except AlationError, error:
        print error


def setup():
    api_setup.run_setup()
