
from wok_hooks.misc import Configuration as _Configuration
from wok_hooks.comments import Post as Comment
import imaplib
import email
import time
import datetime
import re

DEFAULTS = {'server': '',
            'user': '',
            'password': ''}


class Configuration(_Configuration):

    def __init__(self, path, **kwargs):
        _Configuration.__init__(self, path, **kwargs)

        for key, value in DEFAULTS.items():
            if key not in self:
                self[key] = value
                self.save()

email_pattern = re.compile(r'[\w\-]?[<][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}?[>]')


def add_mails_to_comments(options, content_dir=None):

    if content_dir is None:
        content_dir = './content/comments/'

    config = Configuration('comments.config')

    connection = imaplib.IMAP4_SSL(config['server'])
    connection.login(config['user'], config['password'])
    connection.select()

    typ, data = connection.search(None, 'ALL')
    for num in data[0].split():
        typ, data = connection.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)

        slug = email_message['message-id'].replace('<', '').replace('>', '').replace('@', '-').replace('.', '-').lower()
        author = email_message['from']
        author_email = email_pattern.findall(author)[0]
        author = author.replace(author_email, '').strip()
        author_email = author_email.replace('<', '').replace('>', '')
        reference = email_message['subject']
        title = 'Re %s' % reference
        date = time.mktime(email.utils.parsedate(email_message['date']))
        date = datetime.datetime.fromtimestamp(date)
        content = None
        if email_message.get_content_maintype() == 'text':
            content = email_message.get_payload()
        comment = Comment(slug, title, reference, date, author, author_email, content)
        comment.save(content_dir)

    connection.close()
    connection.logout()
