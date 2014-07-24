# core Python packages
import datetime
import logging
import os


# django packages
from django.utils.timezone import utc
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


# local project and app packages
from djhcup_reporting.models import DataSet


# sister app stuff
from djhcup_core.utils import get_pgcnxn


# start a logger
logger = logging.getLogger('default')


# make these tasks app-agnostic with @celery.shared_task
import celery
from celery.result import AsyncResult


@celery.shared_task
def extract_dataset(d_pk, dry_run=False):
    """
    Generates SQL and runs a query to extract a dataset
    """
    # grab the DataSet object
    try:
        d = DataSet.objects.get(pk=d_pk)
    except:
        raise Exception("Unable to find DataSet with pk {pk}" \
            .format(pk=d_pk))
    d.log("tasks.extract_dataset called for d_pk=%s" % d_pk,
          status="IN PROCESS")
    
    # initiate a connection
    # TODO: render this a limited permission account
    # (to prevent sql injection)
    # SECURITY WARNING: this is presently a major risk for malicious behavior
    try:
        cnxn = get_pgcnxn()
    except:
        raise Exception(d.fail("Unable to obtain a database connection."))
    
    try:
        result = d.extract(cnxn, dry_run)
    except:
        d.fail("Failed unexpectedly. Check logs for details.")
        # re-raise
        raise
    
    return result
