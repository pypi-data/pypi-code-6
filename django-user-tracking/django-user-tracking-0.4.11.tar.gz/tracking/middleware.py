from datetime import datetime, timedelta

import re
import traceback

from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.db.utils import DatabaseError
from django.http import Http404

from tracking import utils, settings
from tracking.models import Visitor, UntrackedUserAgent, BannedIP


import logging
log = logging.getLogger('tracking.middleware')

title_re = re.compile('<title>(.*?)</title>')


class VisitorTrackingMiddleware(object):
    """
    Keep track of your active users.  Anytime a visitor accesses a valid URL,
    their unique record will be updated with the page they're on and the last
    time they requested a page.

    Records are considered to be unique when the session key and IP address
    are unique together.  Sometimes the same user used to have two different
    records, so a check to see if the session key had changed for the same IP
    and user agent in the last 5 minutes is added
    """

    def __init__(self):
        """Process the settings before handling the first request."""
        # get a list of URL prefixes that should not be tracked.
        self.prefixes = settings.NO_TRACKING_PREFIXES
        log.info(settings.MEDIA_URL)
        if settings.MEDIA_URL and settings.MEDIA_URL != '/':
            self.prefixes.append(settings.MEDIA_URL)
        if settings.STATIC_URL and settings.STATIC_URL != '/':
            self.prefixes.append(settings.STATIC_URL)

        log.debug('Processed user tracking settings successfully. '
                  'Ready to handle new visitors.')

    def process_request(self, request):
        # don't process AJAX requests
        if request.is_ajax():
            return

        ip_address = utils.get_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]

        # retrieve untracked user agents from cache
        ua_key = '_tracking_untracked_uas'
        untracked = cache.get(ua_key)
        if untracked is None:
            log.debug('Updating untracked user agent cache...')
            untracked = UntrackedUserAgent.objects.all()
            cache.set(ua_key, untracked, 3600)
            log.info('Untracked user agent cache successfully created.')

        # see if the user agent is not supposed to be tracked
        for ua in untracked:
            # if the keyword is found in the user agent, stop tracking
            if user_agent.find(ua.keyword) != -1:
                log.debug('Not tracking UA "%s" because of keyword: %s' %
                          (user_agent, ua.keyword))
                return

        if hasattr(request, 'session') and request.session.session_key:
            # use the current session key if we can
            session_key = request.session.session_key
        else:
            # otherwise just fake a session key
            session_key = '%s:%s' % (ip_address, user_agent)
            session_key = session_key[:40]

        # ensure that the request.path does not begin with any of the prefixes
        for prefix in self.prefixes:
            if request.path.startswith(prefix):
                log.debug('Not tracking request to: %s' % request.path)
                return

        # if we get here, the URL needs to be tracked
        now = datetime.now()

        attributes = {
            'session_key': session_key,
            'ip_address': ip_address
        }

        # see if this is a known visitor, or create a new entry
        try:
            visitor = Visitor.objects.get(**attributes)
        except Visitor.DoesNotExist:
            # see if there's a visitor with the same IP and user agent
            # within the last 5 minutes
            cutoff = now - timedelta(minutes=5)
            visitors = Visitor.objects.filter(
                ip_address=ip_address,
                user_agent=user_agent,
                last_update__gte=cutoff
            )

            if len(visitors):
                visitor = visitors[0]
                visitor.session_key = session_key
                log.debug('Using existing visitor for IP %s / UA %s: %s' %
                          (ip_address, user_agent, visitor.id))
            else:
                # it's probably safe to assume that the visitor is brand new
                visitor = Visitor(**attributes)
                log.debug('Created a new visitor: %s' % attributes)
        except:
            return

        # determine whether or not the user is logged in
        user = request.user
        if isinstance(user, AnonymousUser):
            user = None

        # update the tracking information
        visitor.user = user
        visitor.user_agent = user_agent

        # if the visitor record is new, or the visitor hasn't been here for
        # at least an hour, update their referrer URL
        one_hour_ago = now - timedelta(hours=1)
        if not visitor.last_update or visitor.last_update <= one_hour_ago:
            visitor.referrer = request.META.get('HTTP_REFERER',
                                                'unknown')[:255]

            # reset the number of pages they've been to
            visitor.page_views = 0
            visitor.session_start = now

        visitor.url = request.path
        visitor.page_views += 1
        visitor.last_update = now
        try:
            visitor.save()
        except DatabaseError:
            log.error('Problem when saving visitor information:\n%s\n\n%s' %
                      (traceback.format_exc(), locals()))


class VisitorCleanUpMiddleware:
    """Clean up old visitor tracking records in the database"""

    def process_request(self, request):
        timeout = settings.TRACKING_CLEANUP_TIMEOUT

        if str(timeout).isdigit():
            log.debug('Cleaning up visitors older than %s hours' % timeout)
            timeout = datetime.now() - timedelta(hours=int(timeout))
            Visitor.objects.filter(last_update__lte=timeout).delete()


class BannedIPMiddleware:
    """
    Raise an Http404 error for any page request from a banned IP.  IP addresses
    may be added to the list of banned IPs via the Django admin.

    The banned users do not actually receive the 404 error--instead they get
    an "Internal Server Error", effectively eliminating any access to the site.
    """

    def process_request(self, request):
        key = '_tracking_banned_ips'
        ips = cache.get(key)
        if ips is None:
            # compile a list of all banned IP addresses
            log.debug('Updating banned IPs cache...')
            ips = [b.ip_address for b in BannedIP.objects.all()]
            cache.set(key, ips, 3600)
            log.info('Banned IPs cache successfully created.')

        # check to see if the current user's IP address is in that list
        if utils.get_ip(request) in ips:
            raise Http404
