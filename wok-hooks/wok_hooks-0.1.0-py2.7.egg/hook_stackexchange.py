import logging

from wok_hooks.misc import Configuration as _Configuration

import urllib3

http = urllib3.PoolManager()

from datetime import datetime
import json
from wok_hooks.timeline import Post as TimelineUpdate


class Configuration(_Configuration):
    DEFAULTS = {'accounts': [{'user_id': None, 'site': 'stackoverflow'}]}

    def __init__(self, path, **kwargs):
        _Configuration.__init__(self, path, **kwargs)

        for key, value in self.DEFAULTS.items():
            if key not in self:
                self[key] = value
                self.save()


class StackExchangeActivity(TimelineUpdate):
    def __init__(self, slug, title, url, time, content):
        TimelineUpdate.__init__(self, slug.lower().strip(), title, url, time, content)


class StackExchangeQuestion(StackExchangeActivity):
    def __init__(self, site, user_id, title, creation_date, timeline_type, post_id, slug=None, post_type=None):
        if slug is None:
            slug = '%s-question-%d' % (site, post_id)

        url = 'http://api.stackexchange.com/2.1/posts/%d?order=desc&sort=activity&site=%s' % (post_id, site)
        try:
            response = http.request('GET', url)
            response_struct = json.loads(response.data)
            url = response_struct['items'][0]['link']
        except:
            pass

        content = 'asked question on %s [%s](%s)' % (site, title, url)

        StackExchangeActivity.__init__(self, slug, title, url, datetime.fromtimestamp(creation_date), content)

        self.actions.append(('show question', url))


class StackExchangeAnswer(StackExchangeActivity):
    def __init__(self, site, user_id, title, creation_date, timeline_type, post_id, slug=None, post_type=None):
        if slug is None:
            slug = '%s-answer-%d' % (site, post_id)

        url = 'http://api.stackexchange.com/2.1/posts/%d?order=desc&sort=activity&site=%s' % (post_id, site)
        try:
            response = http.request('GET', url)
            response_struct = json.loads(response.data)
            url = response_struct['items'][0]['link']
        except:
            pass

        content = 'answered on %s [%s](%s)' % (site, title, url)

        StackExchangeActivity.__init__(self, slug, title, url, datetime.fromtimestamp(creation_date), content)

        self.actions.append(('show answer', url))


def add_stackexchange_questions_to_timeline(options, content_dir='./content/timeline/'):
    config = Configuration('stackexchange.config')
    for account in config['accounts']:
        assert account['user_id'], 'user_id must be set in stackexchange.config'
        assert account['site'], 'site must be set in stackexchange.config'
        url = 'http://api.stackexchange.com/2.1/users/%d/timeline?site=%s' % (account['user_id'], account['site'])

        response = http.request('GET', url)
        response_struct = json.loads(response.data)

        if 'items' in response_struct:
            for entry in response_struct['items']:
                if entry['timeline_type'] == 'asked':
                    StackExchangeQuestion(account['site'], **entry).save(content_dir)
                elif entry['timeline_type'] == 'answered':
                    StackExchangeAnswer(account['site'], **entry).save(content_dir)
                else:
                    logging.debug('ingore %s from %s' % (account['site'], entry['timeline_type']))
        else:
            logging.debug('no activities in %s' % account['site'])


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s:%(message)s', level=logging.DEBUG)
    import os

    os.chdir('..')
    add_stackexchange_questions_to_timeline({}, '/tmp/')
