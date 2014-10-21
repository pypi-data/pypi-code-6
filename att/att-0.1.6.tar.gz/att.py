#!/usr/bin/env python

"""AT&T

Usage:
  att.py
  att.py --phone PHONE --code CODE
  att.py --from FROM
  att.py --from FROM --to TO
  att.py --phone PHONE --code CODE --from FROM
  att.py --phone PHONE --code CODE --from FROM --to TO
  att.py (-h | --help)
  att.py --version

Options:
  -h --help         Show this screen.
  -v --version      Show version.
  -p --phone        Phone number.
  -c --code         AT&T 4 digits code.
  -f --from         Date from (MM/DD/YYYY).
  -t --to           Date to (MM/DD/YYYY).

"""

import os
import sys
import requests
import arrow
import json
from bs4 import BeautifulSoup
from docopt import docopt


__version__ = '0.1.6'


class Att:
    def __init__(self, phone, code):
        self.session = requests.Session()
        self.endpoint = 'https://www.paygonline.com/websc'
        self.login(phone, code)


    def login(self, phone, code):
        r = self.session.post('%s/logon.html' % self.endpoint, {'phoneNumber': phone, 'password': code})
        soup = BeautifulSoup(r.text)
        err = soup.find(id="error")
        if err:
            print err.find('p').text.strip()
            sys.exit(0)


    def getFormToken(self):
        r = self.session.get('%s/history.html' % self.endpoint)
        soup = BeautifulSoup(r.text)
        return soup.find('input', {'name': 'struts.token'}).get('value')


    def getEvents(self, event_type, date_from, date_to):
        if isinstance(date_from, arrow.arrow.Arrow):
            date_from = date_from.format('MM/DD/YY')
        if isinstance(date_to, arrow.arrow.Arrow):
            date_to = date_to.format('MM/DD/YYYY')
        payload = {
            'struts.token.name': 'struts.token',
            'struts.token': self.getFormToken(),
            'datefrom': date_from,
            'dateto': date_to,
            'historyTypeCode': event_type,
        }
        r = self.session.post('%s/historyrequest.html' % self.endpoint, payload)
        soup = BeautifulSoup(r.text)
        err = soup.find(id="error")
        if err:
            print err.find('p').text.strip()
            sys.exit(0)
        calls = soup.find_all('div', {'class': 'property-details'})
        results = []

        def getContent(divs, idx):
            return divs[idx].contents[1].text.strip()

        for call in calls:
            rows = call.find_all('div', {'class': 'row'})
            divs = rows[1].find_all('div')
            result = {'type': getContent(divs, 1),
                      'nature_of_call': getContent(divs, 3),
                      'number_called': getContent(divs, 5),
                      'calling_number': getContent(divs, 7),
                      'date': str(arrow.get('%s %s' % (getContent(divs, 9), getContent(divs, 11)), 'MM/DD/YY HH:mm:ss A').datetime),
                      'timezone': getContent(divs, 13),
                      'duration': getContent(divs, 15),
                      'total_amount': int(round(float(getContent(divs, 17).strip('$'))*100)),
                      'service_used': getContent(divs, 19),
                      'units_charged': getContent(divs, 21),
                      'call_location': getContent(divs, 23),
                     }
            results.append(result)
        return results


    def getVoices(self, date_from, date_to):
        return self.getEvents('VOICE', date_from, date_to)


    def getMessaging(self, date_from, date_to):
        return self.getEvents('DATA_MESSAGING', date_from, date_to)


    def getAllEvents(self, date_from, date_to):
        return self.getVoices(date_from, date_to) + self.getMessaging(date_from, date_to)


def main():
    args = docopt(__doc__, version=__version__)
    PHONE = args.get('PHONE') or os.environ.get('PHONE')
    CODE = args.get('CODE') or os.environ.get('CODE')
    DATE_FROM = args.get('FROM') or arrow.now().replace(months=-1)
    DATE_TO = args.get('TO') or arrow.now()

    att = Att(PHONE, CODE)
    print json.dumps(att.getAllEvents(DATE_FROM, DATE_TO))


if __name__ == '__main__':
    main()
