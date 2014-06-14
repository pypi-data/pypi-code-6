# -*- coding: utf_8 -*-

import urllib2
from StringIO import StringIO
from zipfile import ZipFile
from collections import OrderedDict
import json

from bs4 import BeautifulSoup

URL = 'http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_megase.zip'

class Megasena():
    """Megasena class."""

    def __init__(self):
        pass

    def get_results(self):
        """Download the megasena results zip file from URL and unzip it
        to a memory file.
        """
        u = urllib2.build_opener(urllib2.HTTPCookieProcessor()).open(URL)
        z = ZipFile(StringIO(u.read()))
        self.html = StringIO(z.open(z.namelist()[0]).read())

    def parse_header(self):
        """Parse the megasena header from the html table and returns a
        list.
        """
        try:
            rows = BeautifulSoup(self.html.read()).find('table').findAll('tr')
        except AttributeError:
            self.html.seek(0)
            rows = BeautifulSoup(self.html.read()).find('table').findAll('tr')

        header = list()
        for tr in rows:
            cols = tr.findAll('th')
            for th in cols:
                header.append(th.find(text=True).lower().replace(' ', '_'))

        return header

    def parse_results(self):
        """Parse the megasena results from the html table and assigns
        it to the 'json' variable.
        """
        header = self.parse_header()
        try:
            rows = BeautifulSoup(self.html.read()).find('table').findAll('tr')
        except AttributeError:
            self.html.seek(0)
            rows = BeautifulSoup(self.html.read()).find('table').findAll('tr')

        results = list()
        for tr in rows:
            od = OrderedDict()
            cols = tr.findAll('td')
            for index, td in enumerate(cols):
                od[header[index]] = td.find(text=True)
            results.append(od)

        self.json = StringIO(json.dumps(results, indent=4))

    def get_json(self):
        """Reads the results in json and returns it in python
        format.
        """
        try:
            results_in_json = json.loads(self.json.read())
        # self.json has been read, so it must return to the start.
        except ValueError:
            self.json.seek(0)
            results_in_json = json.loads(self.json.read())
        return results_in_json

    def most_drawn_number_by_position(self):
        """Returns the most frequently drawn number by position,
        varying from the first to the sixth position.
        """
        results_in_json = self.get_json()

        # Each list represents a dozen by position (1st, ..., 6th).
        dozens = [[],[],[],[],[],[],]
        for contest in results_in_json:
            if contest:   # The first dictionary is empty.
                dozens[0].append(contest[u'1\u00aa_dezena'])
                dozens[1].append(contest[u'2\u00aa_dezena'])
                dozens[2].append(contest[u'3\u00aa_dezena'])
                dozens[3].append(contest[u'4\u00aa_dezena'])
                dozens[4].append(contest[u'5\u00aa_dezena'])
                dozens[5].append(contest[u'6\u00aa_dezena'])

        # Counts the times a certain dozen has been drawn in that
        # particular position (1st, ..., 6th).
        counted_dozens = []
        for dozen in dozens:
            dozens_count = {}
            for d in dozen:
                dozens_count[d] = dozens_count.get(d, 0) + 1
            counted_dozens.append(dozens_count)

        # Sort the dozens in descending order by position and saves the
        # first (does not consider a tie).
        most_drawn = OrderedDict()
        for drawing_position in counted_dozens:
            for dozen in sorted(drawing_position,
                            key=drawing_position.get,
                            reverse=True):
                most_drawn[dozen] = drawing_position[dozen]
                break

        return json.dumps(most_drawn, indent=4)

    def most_drawn_number_by_contest(self):
        """Returns the most frequently drawn number among all
        contests.
        """
        results_in_json = self.get_json()

        numbers = list()
        for contest in results_in_json:
            if contest:   # The first dictionary is empty.
                for dozen in [u'1\u00aa_dezena', u'2\u00aa_dezena',
                              u'3\u00aa_dezena', u'4\u00aa_dezena',
                              u'5\u00aa_dezena', u'6\u00aa_dezena']:
                    numbers.append(contest[dozen])

        numbers_count = dict()
        for number in numbers:
            numbers_count[number] = numbers_count.get(number, 0) + 1

        most_drawn = OrderedDict()
        for number in sorted(numbers_count,
                             key=numbers_count.get,
                             reverse=True):
            most_drawn[number] = numbers_count[number]

        return json.dumps(most_drawn, indent=4)

    def check_drawn_dozens(self, dozens):
        """Check if the numbers received in the list of dozens have
        been drawn ever.
        """
        dozens = sorted(dozens)
        results_in_json = self.get_json()

        contest_list = list()
        for contest in results_in_json:
            if contest:   # The first dictionary is empty.
                checked_dozens = list()
                for dozen in [u'1\u00aa_dezena', u'2\u00aa_dezena',
                              u'3\u00aa_dezena', u'4\u00aa_dezena',
                              u'5\u00aa_dezena', u'6\u00aa_dezena']:
                    checked_dozens.append(int(contest[dozen]))
                checked_dozens = sorted(checked_dozens)
                if dozens == checked_dozens:
                    contest_list.append(contest['concurso'])

        return contest_list
