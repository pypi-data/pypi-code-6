# -*- coding: utf-8 -*-
"""
install requests using::

    pip install requests

example use in hooks::

    call = load_extension('push_post.py')
    if call:
        kwargs = dict()
        kwargs['URL'] = <url for post data> # an endpoint url data will be sent to
        call(**kwargs)

"""
import urllib
import urllib2


def run(*args, **kwargs):
    """
    Extra params

    :param URL: url to send the data to
    """

    url = kwargs.pop('URL', None)
    if url:
        from rhodecode.lib.compat import json
        from rhodecode.model.db import Repository
        from rhodecode.lib import helpers as h

        repo = Repository.get_by_repo_name(kwargs['repository'])
        changesets = []
        vcs_repo = repo.scm_instance_no_cache()
        for r in kwargs['pushed_revs']:
            cs = vcs_repo.get_changeset(r)
            changesets.append(json.dumps(cs))

        kwargs['pushed_revs'] = changesets
        headers = {
            'User-Agent': 'RhodeCode-SCM web hook',
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
            'Accept-Encoding': 'gzip,deflate,sdch',
        }

        data = kwargs
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        the_page = response.read()
        return 0
