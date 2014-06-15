"""
.. _thread-local:

thread_local
============

this middleware takes the user from a request and places it into a
threadlocal, so it can be retrieved in other contests

Stolen from a mail to django usergroup by Luke Plant - 17.6.2006

.. autofunction:: get_current_user

"""
from threading import local
from django.contrib.auth.models import AnonymousUser

_thread_locals = local()
_anonymous = AnonymousUser()

def get_current_user():
    """Return the user in the current thread
    
    Tipical usage::

        from jmb.core.middleware.thread_local import get_current_user
        user = get_current_user()

    When working in the shell you can pretend you are a user using setting 
    INTERACTIVE_USER in django.conf.settings. That's easily done via the
    :func:`jmb.core.conf.set_interactive_user` :: 

        from jmb.core.conf import set_interactive_user
        set_interactive_user('admin')


    """
    user = getattr(_thread_locals, 'user',  None)
    if user:
        return user
    else:
        # permette di usare jumbo.conf.set_interactive_user
        from django.conf import settings
        return getattr(settings, 'INTERACTIVE_USER', _anonymous)

def get_request():
    request = getattr(_thread_locals, 'request', None)
    return request

class ThreadLocals(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""
    def process_request(self, request):
        _thread_locals.request = request
        _thread_locals.user = getattr(request, 'user', None)

