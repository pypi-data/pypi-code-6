# -*- coding: utf-8 -*-
"""
install requests using::

    pip install requests

example use in hooks::

    call = load_extension('slack.py')
    if call:
        call_kwargs = dict()
        # pass in the hook arguments
        call_kwargs.update(kwargs)
        call_kwargs['SLACK_ROOM'] = <room>   # your target channel for notification
        call_kwargs['SLACK_TOKEN'] = <token> # slack API TOKEN
        call_kwargs['SLACK_FROM'] = <from>   # display user who does the notification
        call(**call_kwargs)

"""
import json
import requests
import urlparse


BASE_URL = 'https://slack.com/api/'
INCOMING_WEBHOOK_URL = ''
API_VERSION = 1


class SlackApi(object):
    def __init__(self, auth_token, base_url=BASE_URL, api_version=API_VERSION):
        self._auth_token = auth_token
        self._base_url = base_url
        self._api_version = api_version

    def message(self, call_kwargs):
        api_endpoint = urlparse.urljoin(self._base_url, 'chat.postMessage')

        payload = {}
        payload.update(call_kwargs)
        resp = requests.post(api_endpoint, data=payload,
                             params={'token': self._auth_token})

        json_resp = resp.json()

        if json_resp.get('ok') in [False]:
            raise Exception(json_resp.get('error'))
        else:
            return resp.json()


class IncomingWebHookCall(object):

    def __init__(self, base_url=INCOMING_WEBHOOK_URL):
        self._base_url = base_url

    def message(self, payload):
        api_endpoint = self._base_url

        resp = requests.post(api_endpoint, data=json.dumps(payload),)

        if resp.status_code != 200:
            raise Exception('Failed to post due to error %s' % (resp.text,))

        json_resp = resp

        if json_resp.text != 'ok':
            raise Exception(json_resp.get('error'))
        else:
            return resp


def _escaper(text):
    """
    & replaced with &amp;
    < replaced with &lt;
    > replaced with &gt;
    """
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def run(*args, **kwargs):
    from rhodecode.model.db import Repository
    from rhodecode.lib import helpers as h

    ## HIPCHAT CONFIGURATION
    SLACK_ROOM = kwargs.pop('SLACK_ROOM', None)  # your target channel for announcements
    SLACK_TOKEN = kwargs.pop('SLACK_TOKEN', None)  # slack API TOKEN
    SLACK_FROM = kwargs.pop('SLACK_FROM', None)  # user who does the announcements
    _INCOMING_WEBHOOK_URL = kwargs.pop('INCOMING_WEBHOOK_URL', None)  # using webhooks for posting to channel
    SLACK_FROM_ICON_URL = kwargs.pop('SLACK_FROM_ICON_URL', None)  # special icon to use for a bot

    if not (SLACK_ROOM and SLACK_TOKEN and SLACK_FROM):
        print 'Missing SLACK_ROOM or SLACK_TOKEN or SLACK_FROM parameters'
        return 0

    def link_to_commit(repo_url, rev, message):
        rev_url = '%s/changeset/%s' % (repo_url, rev)
        _message = h.shorter(h.urlify_commit(message.rstrip('\n')), 200)
        return "<%s|%s> - %s" % (rev_url, rev[:6], _message)

    def header(username, branch, repo_name, repo_url):
        repo_url = '<%s|%s>' % (repo_url, repo_name)
        return ('*%(username)s* pushed to %(branch)s branch in %(repo_url)s'
                % {'username': username, 'branch': branch, 'repo_url': repo_url})

    repo = Repository.get_by_repo_name(kwargs['repository'])
    repo_url = '%(server_url)s/%(repository)s' % kwargs

    changesets = []
    # extract the branch
    branch = None
    vcs_repo = repo.scm_instance_no_cache()
    for r in kwargs['pushed_revs']:
        cs = vcs_repo.get_changeset(r)
        changesets.append(cs)
        if branch is None:
            branch = cs.branch

    msg = []
    msg.append(header(kwargs['username'], branch, repo.repo_name, repo_url))

    for cs in changesets:
        msg.append(link_to_commit(repo_url, cs.raw_id, cs.message))

    msg = '\n'.join(msg)
    slackapi = IncomingWebHookCall(_INCOMING_WEBHOOK_URL)

    _payload = {
        'channel': SLACK_ROOM,
        'username': SLACK_FROM,
        'text': h.shorter(msg, 1024*5),
    }
    if SLACK_FROM_ICON_URL:
        _payload.update({'icon_url': SLACK_FROM_ICON_URL,})
    slackapi.message(_payload)

    return 0
