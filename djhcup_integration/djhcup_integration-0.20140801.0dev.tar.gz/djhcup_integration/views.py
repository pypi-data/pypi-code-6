# core Python packages
import logging


# third party packages


# django packages
from django.shortcuts import render
from django.utils.timezone import utc
from django.contrib.auth.decorators import login_required


# local imports


# start a logger
logger = logging.getLogger('default')


# Create your views here.
@login_required(login_url='/login/')
def index(request):
    logger.debug('Integration index requested')
    
    context = {
        'title': 'The Django-HCUP Hachoir: Integration Index',
    }
    
    template = 'djhcup_base.html'
    return render(request, template, context)
