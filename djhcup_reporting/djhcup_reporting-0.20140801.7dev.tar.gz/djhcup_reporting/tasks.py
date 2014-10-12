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
def process_dataset(d_pk, dry_run=False):
    """
    Extracts dataset and bundles into a ZIP archive
    for download.
    """
    # grab the DataSet object
    try:
        d = DataSet.objects.get(pk=d_pk)
    except:
        raise Exception("Unable to find DataSet with pk {pk}" \
            .format(pk=d_pk))
    d.log("tasks.process_dataset called for d_pk=%s" % d_pk,
          status="IN PROCESS")
    d.save()
    
    try:
        result = d._process(dry_run)
    except:
        d.fail("DataSet._process() failed unexpectedly. Check logs for details.")
        # re-raise
        raise
    
    return result
