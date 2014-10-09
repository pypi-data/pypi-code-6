
import logging


class Post(object):

    def __init__(self, slug, title, reference, time, author, author_email, content):
        self.slug = slug
        self.title = title
        self.reference = reference
        self.author = author
        self.author_email = author_email
        self.time = time
        self.content = content

    def save(self, content_dir):
        with open('%s%s.md' % (content_dir, self.slug), 'w+') as fd:
            def writeline(text):
                try:
                    fd.write(text.encode('utf8') + '\n')
                except Exception as ex:
                    logging.error(ex)
            writeline('title: %s' % self.title)
            writeline('slug: %s' % self.slug)
            writeline('category: %s' % self.reference)
            writeline('type: comment')
            writeline('datetime: %s' % self.time.isoformat(' '))
            writeline('author: %s' % self.author)
            writeline('author_email: %s' % self.author_email)
            writeline('---')
            writeline(self.content)
