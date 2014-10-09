import logging

from wok_hooks.misc import Configuration as _Configuration

import feedparser
from datetime import datetime
from wok_hooks.timeline import Post as TimelineUpdate


class Configuration(_Configuration):
    DEFAULTS = {'secret_user_id': None}

    def __init__(self, path, **kwargs):
        _Configuration.__init__(self, path, **kwargs)

        for key, value in self.DEFAULTS.items():
            if key not in self:
                self[key] = value
                self.save()


class Digg(TimelineUpdate):
    def __init__(self, time, title, url):
        slug = str(filter(unicode.isalnum, url.replace('http://', ''))).lower()

        content = 'recommended [%s](%s)' % (title, url)

        TimelineUpdate.__init__(self, slug, title, url, time, content)

        self.actions.append(('show article', url))


def add_diggs_to_timeline(options, content_dir='./content/timeline/'):
    config = Configuration('digg.config')
    url = 'http://digg.com/user/%(secret_user_id)s/diggs.rss' % {'secret_user_id': config['secret_user_id']}

    for entry in feedparser.parse(url).entries:
        time, title, link = datetime(*entry.published_parsed[:6]), entry.title, entry.link
        Digg(time, title, link).save(content_dir)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s:%(message)s', level=logging.DEBUG)
    import os

    os.chdir('..')
    add_diggs_to_timeline({}, '/tmp/')
