import api_setup_client as api_setup
import api_request_client as api
import argparse
import sys


def get_sql(*args):
    try:
        qid = int(sys.argv[1])
        print api.get_query_sql(qid)
    except ValueError:
        print "Not a valid integer for query id"


def get_result(*args):
    try:
        rid = int(sys.argv[1])
        print api.get_result_csv(qid)
    except ValueError:
        print "Not a valid integer for result id"


def setup():
    api_setup.run_setup()
