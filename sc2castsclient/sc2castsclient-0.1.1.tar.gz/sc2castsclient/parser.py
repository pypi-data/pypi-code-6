#!/usr/bin/env python

import re
from bs4 import BeautifulSoup
import requests

from model import *

# ONLY does parsing; use something else to get the URL and pass it in as an html string
# this class is ordered by the navigation on sc2casts.com
class Sc2CastsParser(object):

    @staticmethod
    def _cleanup_path(path):
        ''' ensures that there is exactly one leading /, for building urls '''
        if not path.startswith('/'):
            return '/' + path
        return path

    # Best of 5
    # Best of 3 - All in 1 video
    # BO3 in 1 Video
    @staticmethod
    def _best_of(series_name):
        try:
            best_of_string = re.search('\((.*)\)', series_name).group(1)

            ''' returns: int, the number of games there are '''
            # case by case
            if '1 game' in best_of_string.lower():
                num_videos = 1
                best_of = 1
            elif 'best of ' in best_of_string.lower():
                num_videos = int(re.search('Best of (\d+)', best_of_string).group(1))
                best_of = num_videos
            elif 'bo' in best_of_string.lower():
                num_videos = int(re.search('BO(\d+)', best_of_string).group(1))
                best_of = num_videos
            else:
                num_videos = -1
                best_of = -1
            return best_of
        except AttributeError as e:
            # regex failed; either there's no best_of info in the name, or it's a new pattern
            return 'Unknown BestOf'

    def _parse_series_page(self, series_page_html):
        series = Sc2CastsSeries()
        soup = BeautifulSoup(series_page_html)

        # useful 'global' fields
        vs_label = soup.find('div', class_='vslabel')
        info_label = soup.find('div', class_='infolabel')

        # the series 'header' and metainfo

        # what a pain in the ass.
        # note that we manually add the "(best of ..)" info here, to maximize code reuse
        def name(vs_label, info_label):
            return '{0} ({1})'.format(vs_label.h1.text, info_label.h2.text)
        series.name = name(vs_label, info_label)
        series.path = None

        # first span: TODO convert to object
        def matchup(vs_label):
            try:
                images = vs_label.find_all('img')
                (left, right) = (images[0], images[1])
                (left_title, right_title) = (left['title'], right['title'])

                return "{0}v{1}".format(left_title[0:1], right_title[0:1])
            except Exception as e:
                # no matchup; probably team versus team
                return ''
        series.matchup = matchup(vs_label)

        def players(vs_label):
            return [
                Sc2CastsPlayer(name=a.b.text, path=a['href'])
                for a in vs_label.h1.find_all('a')
            ]
        series.players = players(vs_label)
        series.players_desc = None

        series.best_of = self._best_of(series.name)
        # will set this later
        series.num_videos = -2

        def event_info(info_label):
            return Sc2CastsEvent(
                name=info_label.find('span', class_='event_name').text,
                path=info_label.find('span', class_='event_name').parent['href'],
            )
        series.event = event_info(info_label)
        series.event_round = info_label.find('span', class_='round_name').text

        def casters(info_label):
            return [
                Sc2CastsCaster(
                    name=span.text,
                    path=span.parent['href'],
                ) for span in info_label.find_all('span', class_='caster_name')
            ]
        series.casters = casters(info_label)
        series.casters_desc = None

        # the last span in the breadcrumb...
        # TODO as datetime obj
        # TODO no longer available; now only has post_date
        def cast_date(breadcrumb):
            return breadcrumb.find_all('span')[-1].text
        def post_date(info_label):
            return info_label.find_all('span')[-1].text
        series.cast_date = None
        series.post_date = post_date(info_label)

        def scores_info(soup):
            scores_el = soup.find('div', id='tt')
            return {
                'up': int(scores_el.find('img', title='Yea').parent.parent.text),
                'down': int(scores_el.find('img', title='Nah').parent.parent.text),
            }
        series.score_up = scores_info(soup)['up']
        series.score_down = scores_info(soup)['down']

        # now we can finally do the casts themselves
        series.casts = [ ]
        for i, iframe in enumerate(soup.find_all('iframe')):
            cast = Sc2CastsCast()

            cast.name = 'Game ' + str(i + 1)
            def source(iframe):
                if 'youtube.com' in iframe['src'].lower():
                    return 'YouTube'
                return 'Unknown'
            cast.source = source(iframe)
            cast.video_url = iframe['src']
            # remove any query params
            if '?' in cast.video_url:
                cast.video_url = cast.video_url.rsplit('?', 1)[0]
            cast.video_id = cast.video_url.rsplit('/', 1)[-1]

            series.casts.append(cast)
        # now that we know now many
        series.num_videos = len(series.casts)

        return series

    def _parse_series_div(self, div):
        series = Sc2CastsSeries()

        def name(div):
            return div.find('a').get_text()
        series.name = name(div)

        def path(div):
            try:
                # index page has it as an h2
                return div.h2.a['href']
            except:
                # top pages and all has it as an h3
                return div.h3.a['href']
        series.path = path(div)

        # team matches don't have the matchup tag, fill with a dummy matchup object
        def matchup(div):
            span = div.find('span', style='color:#cccccc')
            return Sc2CastsMatchup(name=span.text)
        series.matchup = matchup(div)

        def players(div):
            return [
                # no path here, just the name
                Sc2CastsPlayer(name=b.text)
                for b in div.find_all('b')
            ]
        series.players = players(div)
        series.players_desc = None

        series.best_of = self._best_of(series.name)
        # can't be known; default is 0 to match with length of casts
        series.num_videos = 0

        def event(div):
            return Sc2CastsEvent(
                name=div.select('.event_name')[0].string,
                path=div.select('.event_name')[0].parent['href']
            )
        series.event = event(div)
        series.event_round = div.find('span', class_='round_name').text

        def casters(div):
            return [
                Sc2CastsCaster(
                    name=span.text,
                    path=span.parent['href'],
                ) for span in div.find_all('span', class_='caster_name')
            ]
        series.casters = casters(div)
        series.casters_desc = None

        series.cast_date = None

        series.score_up = -1
        series.score_down = -1

        # the actual casts themselves
        # can't find out
        series.casts = [ ]

        def source(div):
            return div.img['alt']

        return series

    def _parse_index(self, top_page_html):
        results = [ ]
        soup = BeautifulSoup(top_page_html)

        for div in soup.find_all('div', class_='latest_series'):
            result = self._parse_series_div(div)
            results.append(result)

        return results

    def _parse_top(self, top_page_html):
        results = [ ]
        soup = BeautifulSoup(top_page_html)

        for div in soup.find_all('div', class_='latest_series'):
            result = self._parse_series_div(div)
            results.append(result)

        return results

    def _parse_all(self, all_page_html):
        results = [ ]
        soup = BeautifulSoup(all_page_html)

        #content_div = soup.select('div .content')[0]
        #for div in content_div.find_all('div', recursive=False):
        for div in soup.find_all('div', class_='latest_series'):
            result = self._parse_series_div(div)
            results.append(result)

        return results

    # in: a section name; there are 4 'valign=top' fields:
    # events: prominent and all events
    # players: notable and all players
    # casters: prominent and all casters
    # matchups: matchups
    #
    # out: the `td` tag containing the given section
    def _parse_browse_page(self, browse_page_html, section_name):
        soup = BeautifulSoup(browse_page_html)

        section_id = {
            'events': 0,
            'players': 1,
            'casters': 2,
            'matchups': 3,
        }[section_name]

        content_div = soup.find_all('td', attrs={ 'valign': 'top' })[section_id]
        return content_div

    def casters(self, html):
        results = [ ]

        for anchor in self._parse_browse_page(html, 'casters').find_all('a'):
            result = Sc2CastsCaster()
            result.name = anchor.string
            result.path = self._cleanup_path(anchor['href'])

            results.append(result)

        return results

    def events(self, html):
        results = [ ]

        for anchor in self._parse_browse_page(html, 'events').find_all('a'):
            result = Sc2CastsEvent()
            result.name = anchor.string
            result.path = self._cleanup_path(anchor['href'])

            results.append(result)

        return results

    def matchups(self, html):
        results = [ ]

        for anchor in self._parse_browse_page(html, 'matchups').find_all('a'):
            result = Sc2CastsMatchup()
            result.name = anchor.string
            result.path = self._cleanup_path(anchor['href'])

            results.append(result)

        return results

    def players(self, html, filter='all'):
        results = [ ]

        # this is a little more annoying; has to be done linearly/statefully since <br> is the separator
        current = Sc2CastsPlayer()
        for el in self._parse_browse_page(html, 'players').children:
            # separator between 'Notable Players' and 'All Players'
            if el.name == 'span' and el.text == 'All Players':
                break

            # save the current and start a new one
            if el.name == 'br':
                # if there's not enough info for this player, don't add it
                if current.name:
                    results.append(current)
                current = Sc2CastsPlayer()

            if el.name == 'a':
                current.sc2ranks_link = el['href']
            if el.name == 'h3':
                current.name = el.a.text
                current.path = self._cleanup_path(el.a['href'])

        # TODO even more annoying that 'All Players' is embedded
        '''
        for anchor in self._parse_browse_page(html, 'players').find_all('a'):
            #print anchor
            #results.append({
                #'desc': anchor.string,
                #'path': anchor['href'],
            #})
            result = Sc2CastsPlayer()
            result.name = anchor.string
            result.path = self._cleanup_path(anchor['href'])

            results.append(result)
        '''

        return results

    def log(self, msg):
        print msg
