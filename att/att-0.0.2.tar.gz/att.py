#!/usr/bin/env python

import os
import sys
import requests
import arrow
from bs4 import BeautifulSoup
from pymongo import MongoClient


__version__ = '0.0.2'


PHONE = os.environ.get('PHONE')
PASSWORD = os.environ.get('PASSWORD')
DATE_FROM = '10/16/2014'
DATE_TO = '10/20/2014'


class Att:
    def __init__(self, phone, password):
        self.session = requests.Session()
        self.phone = phone
        self.password = password
        self.endpoint = 'https://www.paygonline.com/websc'
        self.login()


    def login(self):
        r = self.session.post('%s/logon.html' % self.endpoint, {'phoneNumber': PHONE, 'password': PASSWORD})
        soup = BeautifulSoup(r.text)
        err = soup.find(id="error")
        if err:
            print err.find('p').text.strip()
            sys.exit(0)


    def getFormToken(self):
        r = self.session.get('%s/history.html' % self.endpoint)
        soup = BeautifulSoup(r.text)
        return soup.find('input', {'name': 'struts.token'}).get('value')


    def getEvents(self, event_type):
        payload = {
            'struts.token.name': 'struts.token',
            'struts.token': self.getFormToken(),
            'datefrom': DATE_FROM,
            'dateto': DATE_TO,
            'historyTypeCode': event_type,
        }
        r = self.session.post('%s/historyrequest.html' % self.endpoint, payload)
        soup = BeautifulSoup(r.text)
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


    def getVoices(self):
        return self.getEvents('VOICE')


    def getMessaging(self):
        return self.getEvents('DATA_MESSAGING')


def main():
    att = Att(PHONE, PASSWORD)
    evts = att.getVoices()
    evts += att.getMessaging()

    client = MongoClient()
    db = client.test_database
    events = db.events
    count = 0
    for evt in evts:
        key = {'type': evt['type'], 'date': evt['date']}
        res = events.update(key, evt, True)
        if not res['updatedExisting']:
            count += 1

    print '%s documents fetched' % len(evts)
    print '%s new documents' % count


if __name__ == '__main__':
    main()
