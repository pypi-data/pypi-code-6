#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sqlite3
import sys
import re
import os
import json

import requests
from bs4 import BeautifulSoup
from terminal import Command

# Set default encoding from ascii to utf-8
reload(sys)
if hasattr(sys, 'setdefaultencoding'):
    sys.setdefaultencoding('utf-8')

# User-agent is necessary, or it'll occur `KeyError: 'data' `.
s = requests.session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; \
                   rv:28.0) Gecko/20100101 Firefox/28.0'})


def translate(raw_title):
    '''translate escape characters to utf-8

    To support chinese in log.'''
    def trans(unicode):
        return unichr(int(unicode, 16)).encode('utf-8')

    if '&#x' not in raw_title:
        return raw_title
    characters = re.findall(r'(?<=&#x).{4}', raw_title)
    date = raw_title.split(';')[-1]

    title = ''
    for character in characters:
        title = title + trans(character)
    return title + date


def get_hidden_form_data(page):
    '''Get hidden form data from the page after you click the signin button

    Those data are needed to post to sign in.'''
    hidden_form_data = dict()
    input_tags = page.findAll('input', type='hidden')
    for tag in input_tags:
        hidden_form_data[tag['name']] = tag['value']
    return hidden_form_data


def login(config):
    '''To login in to amazom.com

    The long url is the 'sign in' botton, the short is the 'sign in our
    secure sever' botton.'''

    logging.info('Login...')
    print 'Login...'
    login_url = ('https://www.amazon.com/ap/signin?_encoding=UTF8&openid.assoc'
                 '_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.n'
                 'et%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%'
                 '2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openi'
                 'd.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net'
                 '%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2'
                 'Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.r'
                 'eturn_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhom'
                 'e%3Fie%3DUTF8%26ref_%3Dgno_signin')
    login_post_url = 'https://www.amazon.com/ap/signin'
    login_page = BeautifulSoup(s.get(login_url).text)
    data = get_hidden_form_data(login_page)
    data.update({'email': config['email'], 'password': config['password']})
    s.post(login_post_url, data)


def get_contents(config):
    url = ('https://www.amazon.com/gp/digital/fiona/manage/features/'
           'order-history/ajax/queryPdocs.html')
    r = s.post(url, {'offset': 0, 'count': config['count'],
                     'contentType': 'Personal Document',
                     'queryToken': 0, 'isAjax': 1})
    return [{'category': item['category'], 'contentName': item['asin'],
             'title': item['title']} for item in r.json()['data']['items']]


def get_deviceID():
    r = s.post('https://www.amazon.com/mn/dcw/myx/ajax-activity',
               data={'data' :'{"param":{"GetDevices":{}}}'})
    deviceID = r.json()['GetDevices']['devices'][0]['deviceAccountId']
    return deviceID


def deliver_content(content):
    url = ('https://www.amazon.com/gp/digital/fiona/content-download/'
           'fiona-ajax.html/ref=kinw_myk_ro_send')
    content.update({'isAjax': '1', 'deviceID': get_deviceID()})
    r = s.post(url, content)
    assert r.json()['data'] == 1    # Whether successfully delivered it or not


def deliver_all(contents, db):
    '''Deliver all the contents which haven't been delivered before

    Once delivered it, save it's asin in database.'''

    logging.info('Delivering...')
    print 'Delivering...'

    cursor = db.cursor()
    def contentInDB(content):
        try:
            cursor.execute('select * from content where name = "%s"' % content)
        except sqlite3.OperationalError:
            cursor.execute('create table content (name text)')
            return False
        else:
            return False if cursor.fetchone() is None else True

    contents = filter(lambda x: not contentInDB(x['contentName']), contents)
    for content in contents:
        try:
            logging.info('delivering ' + translate(content['title']))
            print 'delivering ' + translate(content['title'])
            deliver_content(content)
        except:
            logging.error('Error, ignore')
            print 'Error, ignore'
        else:
            logging.info('Done. Save to db.')
            print 'Done. Save to db.'
            cursor.execute('insert into content values ("%s")' %
                           content['contentName'])
    db.commit()

def main():
    command = Command('kindlepush', 'automatically deliver you doc to your kindle')

    try:
        with open(os.path.join(sys.path[0], 'kindlepush_config.json')) as f:
            config = json.load(f)
    except IOError:
        sys.exit("Check your config file. It should in {0}".format(sys.path[0]))

    @command.action
    def read(number=config['number']):
        """
        read the log file

        :param number: the count of days
        :option number: -n, --number [number]
        """
        file_path = os.path.join(config['directory'], 'kindlepush.log')
        os.system('tail -n {0} {1}'.format(number, file_path))
    command.parse()

    logging.basicConfig(
            filename=os.path.join(config['directory'], 'kindlepush.log'),
            level='INFO',
            format='%(asctime)s [%(levelname)s] %(message)s')
    # Disable unwanted log message from the requests library
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    # Connect to the database lying the directory specified in the config
    db = sqlite3.connect(os.path.join(config['directory'], 'kindlepush.db'))

    if 'read' not in sys.argv:
        try:
            login(config)
            deliver_all(get_contents(config), db)
        except KeyError:
            print 'KeyError, check your config file please.'
        except requests.exceptions.ConnectionError:
            print 'Check your network please.'

if __name__ == '__main__':
    main()
