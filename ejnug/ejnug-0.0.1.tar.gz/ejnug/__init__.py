#!/usr/bin/env python3
import os
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote
import datetime

from unidecode import unidecode
from lxml.html.clean import clean_html
from notmuch import Database, Query
from bottle import Bottle, request, response, \
                   abort, redirect, \
                   view, TEMPLATE_PATH, \
                   static_file

EJNUG_DIR = os.path.split(__file__)[0]
TEMPLATE_PATH.append(os.path.join(EJNUG_DIR, 'views'))
app = Bottle()

@app.route('/')
@view('home')
def home():
    return {}

@app.route('/style.css')
def css():
    return static_file('style.css', root = EJNUG_DIR)

@app.get('/!/<querystr:path>/')
@view('thread')
def search(querystr):
    db = Database()
    query = Query(db, querystr)
    if query.count_messages() == 1:
        message = next(iter(query.search_messages()))
        title = message.get_header('subject')
        try:
            parts = [(i + 1, part.get_filename('No description')) \
                     for i, part in enumerate(message.get_message_parts())]
            body = message.get_part(1)
        except UnicodeDecodeError:
            parts = []
            body = 'There was an encoding problem with this message.'
    else:
        title = 'Results for "%s"' % querystr
        parts = []
        body = None

    return {
        'title': title,
        'parts': parts,
        'body': body,
        'threads': list(hierarchy(query)),
    }

def hierarchy(query):
    for i, thread in enumerate(query.search_threads()):
        yield [subhierarchy(message) for message in thread.get_toplevel_messages()]
        if i >= 100:
            # Stop after 100 threads
            break

def subhierarchy(message):
    '''
    Annoyingly, see the note on "unsafe headers" RFC 2368.
    http://tools.ietf.org/html/rfc2368
    '''
    to = message.get_header('reply-to')
    if to == '':
        to = message.get_header('from')

    subject = message.get_header('subject')
    if not subject.lower().startswith('re'):
        subject = 'RE: ' + subject

    references = message.get_header('references')
    if references != '':
        references = references + '\n'
    references = references + message.get_message_id()
    mailto = {
        'to': to,
        'cc': 'Thomas Levine <public@thomaslevine.com>',
        'subject': subject,
        'references': references,
        'in-reply-to': message.get_message_id(),
        'body': quote('''In reply to: http://mail.thomaslevine.com/!/id:%s/
''' % message.get_message_id())
    }

    d = datetime.datetime.fromtimestamp(message.get_date())
    return {
        'message_id': message.get_message_id(),

        'weekday': d.strftime('%A'),
        'notmuchmonth': d.strftime('%Y-%m'),
        'month': d.strftime('%B'), 
        'notmuchday': d.strftime('%Y-%m-%d'),
        'day': d.strftime('%d'), 
        'notmuchyear': d.strftime('%Y'),
        'year': d.strftime('%Y'), 
        'time': d.strftime('%H:%M UTC'),

        'from': message.get_header('from'),
        'to': message.get_header('to'),
        'mailto': 'mailto:%(to)s?cc=%(cc)s&subject=%(subject)s&references=%(references)s&in-reply-to=%(in-reply-to)s&body=%(body)s' % mailto,
        'subject': message.get_header('subject'),
        'is_match': message.is_match(),
        'replies': [subhierarchy(reply) for reply in message.get_replies()]
    }

@app.get('/!/<querystr:path>/<n:int>')
def attachment(querystr, n):
    db = Database()
    query = Query(db, querystr)
    if query.count_messages() != 1:
        redirect('/!/%s/' % querystr)
    else:
        message = next(iter(query.search_messages()))
        parts = message.get_message_parts()
        i = n - 1
        if i >= len(parts):
            redirect('/!/%s/' % querystr)
        else:
            part = parts[i]
            content_type = part.get_content_type()
            response.content_type = content_type
         #  response.charset = part.get_content_charset()

            fn = part.get_filename()
            if fn != None:
                response.headers['content-disposition'] = 'filename="%s";' % unidecode(fn).replace('"', '')

            payload = message.get_part(n)
            if 'html' in content_type.lower():
                return clean_html(payload)
            else:
                return payload

@app.route('/!')
@app.route('/!/')
def exclaim():
    redirect('/')

@app.route('/!/<querystr:path>')
def slash(querystr):
    redirect('/!/' + querystr.rstrip('/') + '/')
