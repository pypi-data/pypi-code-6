# core Python packages
import logging


# third party packages


# django packages
from django.shortcuts import render
from django.utils.timezone import utc


# local imports
from djhcup_reporting.models import Column, ReportingTable, LookupTable, Universe


# start a logger
logger = logging.getLogger('default')


# Create your views here.
def index(request):
    logger.debug('Reporting index requested')
    
    context = {
        'title': 'The Django-HCUP Hachoir: Reporting Index',
    }
    
    template = 'djhcup_base.html'
    return render(request, template, context)
