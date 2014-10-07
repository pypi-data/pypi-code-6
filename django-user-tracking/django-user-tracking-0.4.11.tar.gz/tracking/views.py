from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, Context, loader
from django.utils.translation import ungettext
from django.views.decorators.cache import never_cache

from tracking.models import Visitor
from tracking import settings

from datetime import datetime
from json import JSONEncoder

import traceback

import logging
log = logging.getLogger('tracking.views')


def update_active_users(request):
    """
    Return a list of all active users.
    """
    if request.is_ajax():
        active = Visitor.objects.active()
        user = getattr(request, 'user', None)

        info = {
            'active': active,
            'registered': active.filter(user__isnull=False),
            'guests': active.filter(user__isnull=True),
            'user': user
        }

        # render the list of active users
        t = loader.get_template('tracking/_active_users.html')
        c = Context(info)
        users = {'users': t.render(c)}

        return HttpResponse(content=JSONEncoder().encode(users))

    # if the request was not made via AJAX, raise a 404
    raise Http404


@never_cache
def get_active_users(request):
    """
    Retrieve a list of active users as plain JSON for easier manipulation
    with JavaScript.
    """
    if request.is_ajax():
        active = Visitor.objects.active().reverse()
        now = datetime.now()

        # we don't put the session key or IP address here for security reasons
        try:
            data = {'users': [
                {'id': v.id,
                 # 'user': v.user,
                 'user_agent': v.user_agent,
                 'referrer': v.referrer,
                 'url': v.url,
                 'page_views': v.page_views,
                 'geoip': v.geoip_data_json,
                 'last_update': (now - v.last_update).seconds,
                 'friendly_time': ', '.join(
                     friendly_time((now - v.last_update).seconds))}
                for v in active]}
        except:
            log.error('There was a problem putting all of '
                      'the visitor data together:\n%s\n\n%s' %
                      (traceback.format_exc(), locals()))
            return HttpResponse(content='{}', content_type='text/javascript')

        response = HttpResponse(content=JSONEncoder().encode(data),
                                content_type='text/javascript')
        response['Content-Length'] = len(response.content)

        return response

    # if the request was not made via AJAX, raise a 404
    raise Http404


def friendly_time(last_update):
    minutes = last_update / 60
    seconds = last_update % 60

    friendly_time = []
    if minutes > 0:
        friendly_time.append(ungettext('%(minutes)i minute',
                                       '%(minutes)i minutes',
                                       minutes) % {'minutes': minutes})
    if seconds > 0:
        friendly_time.append(ungettext('%(seconds)i second',
                                       '%(seconds)i seconds',
                                       seconds) % {'seconds': seconds})

    return friendly_time or 0


def display_map(request, template_name=settings.DEFAULT_TRACKING_TEMPLATE,
                extends_template='base.html'):
    """
    Display a map of recently active users.  Requires a Google Maps API key
    and GeoIP in order to be most effective.
    """

    GOOGLE_MAPS_KEY = getattr(settings, 'GOOGLE_MAPS_KEY', None)

    return render_to_response(template_name,
                              {'GOOGLE_MAPS_KEY': GOOGLE_MAPS_KEY,
                               'template': extends_template},
                              context_instance=RequestContext(request))
