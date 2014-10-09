
import logging
import json


class Post(object):

    def __init__(self, slug, title, url, time, content):
        self.slug = slug
        self.title = title
        self.url = url
        self.time = time
        self.content = content
        self.actions = []

    def save(self, content_dir):
        path = '%s%s.md' % (content_dir, self.slug)
        logging.debug('save %s' % path)
        with open(path, 'w+') as fd:
            def writeline(text):
                try:
                    fd.write(text.encode('utf8') + '\n')
                except Exception as ex:
                    logging.error(ex)
            writeline('title: %s' % self.title)
            writeline('slug: %s' % self.slug)
            writeline('category: timeline')
            writeline('type: base')
            writeline('datetime: %s' % self.time.isoformat(' '))
            writeline('actions: %s' % json.dumps(self.actions))
            writeline('---')
            writeline(self.content)
