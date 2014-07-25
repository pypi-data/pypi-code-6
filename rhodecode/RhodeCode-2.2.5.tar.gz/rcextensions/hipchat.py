# -*- coding: utf-8 -*-
"""
install requests using::

    pip install requests

example use in hooks::

    call = load_extension('hipchat.py')
    if call:
        call_kwargs = dict()
        # pass in the hook arguments
        call_kwargs.update(kwargs)
        call_kwargs['HIPCHAT_ROOM'] = <room>   # your target channel for notification
        call_kwargs['HIPCHAT_TOKEN'] = <token> # hipchat API TOKEN
        call_kwargs['HIPCHAT_FROM'] = <from>   # display user who does the notification
        call(**call_kwargs)

"""
import requests
import json

GETS = {
    'rooms': (
        'history', 'list', 'show'
    ),
    'users': (
        'list', 'show'
    )
}

POSTS = {
    'rooms': (
        'create', 'delete', 'message'
    ),
    'users': (
        'create', 'delete', 'update'
    )
}

API_VERSION = '1'
BASE_URL = 'https://api.hipchat.com/v%(version)s/%(section)s/%(method)s'


class HipChatApi(object):
    """Lightweight Hipchat.com REST API wrapper
    """
    def __init__(self, auth_token, name=None, gets=GETS, posts=POSTS,
                base_url=BASE_URL, api_version=API_VERSION):
        self._auth_token = auth_token
        self._name = name
        self._gets = gets
        self._posts = posts
        self._base_url = base_url
        self._api_version = api_version

    def _request(self, method, params={}):
        if 'auth_token' not in params:
            params['auth_token'] = self._auth_token
        url = self._base_url % {
            'version': self._api_version,
            'section': self._name,
            'method': method
        }
        if method in self._gets[self._name]:
            r = requests.get(url, params=params)
        elif method in self._posts[self._name]:
            r = requests.post(url, params=params)
        return json.loads(r.content)

    def __getattr__(self, attr_name):
        if self._name is None:
            return super(HipChatApi, self).__self_class__(
                auth_token=self._auth_token,
                name=attr_name
            )
        else:
            def wrapper(*args, **kwargs):
                return self._request(attr_name, *args, **kwargs)
            return wrapper

def run(*args, **kwargs):
    from rhodecode.model.db import Repository
    from rhodecode.lib import helpers as h

    ## HIPCHAT CONFIGURATION
    HIPCHAT_ROOM = kwargs.pop('HIPCHAT_ROOM', None)  # your target channel for announcements
    HIPCHAT_TOKEN = kwargs.pop('HIPCHAT_TOKEN', None) # hipchat API TOKEN
    HIPCHAT_FROM = kwargs.pop('HIPCHAT_FROM', None) # user who does the announcements

    if not (HIPCHAT_ROOM and HIPCHAT_TOKEN and HIPCHAT_FROM):
        print 'Missing HIPCHAT_ROOM or HIPCHAT_TOKEN or HIPCHAT_FROM parameters'
        return 0

    repo = Repository.get_by_repo_name(kwargs['repository'])
    repo_url = '%(server_url)s/%(repository)s' % kwargs
    kwargs['repository'] = '<a href="%s">%s</a>' % (repo_url, repo.repo_name)

    msg = []
    changesets = []
    branch = None
    vcs_repo = repo.scm_instance_no_cache()
    for r in kwargs['pushed_revs']:
        cs = vcs_repo.get_changeset(r)
        changesets.append(cs)
        if branch is None:
            branch = cs.branch

    kwargs['branch'] = branch
    msg.append("<b>%(username)s</b> pushed to %(branch)s in %(repository)s<\br>" % kwargs)
    msg.append('<pre>')
    for cs in changesets:
        idurl = '<a href="%s">%s</a>' % (repo_url + '/changeset/' + cs.raw_id,
                                         cs.short_id[:6])
        msg.append('%s: %s \n' % (idurl, h.shorter(
            h.urlify_commit(cs.message.rstrip('\n'), kwargs.get('repository')), 200)))

    msg.append('</pre>')
    msg = ''.join(msg)
    hcapi = HipChatApi(auth_token=HIPCHAT_TOKEN)

    hcapi.rooms.message({
        'room_id': HIPCHAT_ROOM,
        'from': HIPCHAT_FROM,
        'message': h.shorter(msg, 1024*5)
    })

    return 0
