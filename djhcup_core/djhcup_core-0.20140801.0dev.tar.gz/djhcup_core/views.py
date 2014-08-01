# core Python packages
import logging


# third party packages


# django packages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.timezone import utc
from django.contrib import auth
from django.contrib.auth.decorators import login_required


# local imports
import utils

# start a logger
logger = logging.getLogger('default')


# Create your views here.
@login_required(login_url='/login/')
def index(request):
    logger.debug('Core index requested')
    
    # TODO: if not is_staff, user goes to list of their requests only
    
    installed_modules = utils.installed_modules()
    
    logger.debug('Component modules detected:')
    [logger.debug('%s: %s' % (k, v)) for k, v in installed_modules.iteritems()]

    context = {
        'title': 'The Django-HCUP Hachoir: Core Index', 
        'djhcup_components': installed_modules
        }
    
    template = 'djhcup_core_index.html'
    return render(request, template, context)


def login(request, messages=[]):
    logger.debug('Login page requested.')
    form = AuthenticationForm(None, request.POST or None)
    
    if request.user.is_authenticated():
        # log them out before proceeding
        auth.logout(request)
        
    if request.POST:
        # process submitted credentials
        form = AuthenticationForm(None, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                # not a disabled account
                auth.login(request, user)
                nextpage = request.GET.get('next', reverse('index'))
                return HttpResponseRedirect(nextpage)
            else:
                messages.append(dict(
                    type='error',
                    content='Your account has been disabled. Please contact an administrator.'))
        else:
            messages.append(dict(
                type='error',
                content='Unable to log in. Please try again.'))
    
    context = {
        'title': 'The Django-HCUP Hachoir: Login', 
        'form': form,
        'response_messages': messages
        }
    
    template = 'djhcup_login.html'
    return render(request, template, context)


def logout(request):
    logger.debug('Logout page requested.')
    messages = []
    
    if auth.logout(request):
        messages.append(dict(
            type='info',
            content='Successfully logged out.'
            ))
    
    return HttpResponseRedirect(reverse('login'))
