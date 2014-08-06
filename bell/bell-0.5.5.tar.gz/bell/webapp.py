# coding=utf8

"""
bell.webapp
~~~~~~~~~~~

Analyzation results visualization via web app.
"""

from datetime import datetime, timedelta
from os.path import dirname, abspath
import time

from flask import abort, Flask, jsonify, render_template, url_for
from dateutil.parser import parse as parse_date

from bell.base import Service
from bell.configs import configs
from bell.utils import normjoin, PrefixedApp


class WebApp(Service):

    name = 'webapp'

    def __init__(self):
        super(WebApp, self).__init__()
        self.ssdb = None
        self.app = None
        self.default_recent = '3h'

    def initialize(self):
        self.all_series_hashmap = configs['ssdb']['allSeries']['hashmap']
        self.ssdb = self.initialize_ssdb()
        self.initialize_webapp()

    def initialize_webapp(self):
        here_dir = abspath(dirname(__file__))
        webapp_dir = normjoin(here_dir, 'res', 'webapp')
        static_folder = normjoin(webapp_dir, 'static')
        template_folder = normjoin(webapp_dir, 'templates')
        self.app = Flask('bell.webapp', static_folder=static_folder,
                         template_folder=template_folder)
        self.register_url_routes()

    def register_url_routes(self):
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/help', 'help', self.help)
        self.app.add_url_rule('/<name>', 'series', self.series)
        self.app.add_url_rule('/<name>/<recent>', 'series_recent',
                              self.series_recent)
        self.app.add_url_rule('/<name>/<int:limit>', 'series_limit',
                              self.series_limit)
        self.app.add_url_rule('/<name>/around/<around>', 'series_around',
                              self.series_around)
        self.app.add_url_rule('/<name>/around/<around>/<offset>',
                              'series_around_offset',
                              self.series_around_offset)
        self.app.add_url_rule('/api/index', 'api_index', self.api_index)
        self.app.add_url_rule('/api/series/<name>/<recent>',
                              'api_series_recent',
                              self.api_series_recent)
        self.app.add_url_rule('/api/series/<name>/<int:limit>',
                              'api_series_limit', self.api_series_limit)
        self.app.add_url_rule('/api/series/<name>/<int:timestamp>/<offset>',
                              'api_series_around_offset',
                              self.api_series_around_offset)

    def zset_name(self, series_name):
        zset_prefix = configs['ssdb']['series']['zsets']['namePrefix']
        return zset_prefix + series_name

    def parse_time_string(self, time_string):
        mappings = {
            's': 'seconds',
            'm': 'minutes',
            'h': 'hours',
            'd': 'days',
        }
        try:
            num = float(time_string[:-1])
        except ValueError:
            abort(404)
        char = time_string[-1]
        return timedelta(**{mappings[char]: num})

    def format(self, keys):  # cast to [(time, value, status)]
        lst = []
        for key in keys:
            v, s, t = key.split(':')
            lst.append((int(t), float(v), int(s)))
        return lst

    def make_data(self, series, name):
        data = []
        breaks = []

        for timestamp, value, status in series:
            x = timestamp * 1000
            y1 = value
            y2 = value if status else None
            data.append((x, y1, y2))
            if status:
                breaks.append(x)

        stat = self.hget(name)
        icon = self.series_stat_icon(name)
        return dict(data=data, breaks=breaks, stat=stat, icon=icon)

    def hexists(self, key):
        return self.ssdb.hexists(self.all_series_hashmap, key)

    def hgetall(self):
        return self.ssdb.hgetall(self.all_series_hashmap)

    def hget(self, key):
        val = self.ssdb.hget(self.all_series_hashmap, key)
        return int(val)

    def zget_limit(self, zset, limit):
        lst = self.ssdb.zrrange(zset, 0, limit)
        keys = lst[-2::-2]
        return self.format(keys)

    def zget_recent(self, zset, time_string):
        start = datetime.now() - self.parse_time_string(time_string)
        start = time.mktime(start.timetuple())  # cast to timestamp
        keys = self.ssdb.zkeys(zset, '', start, '', -1)
        return self.format(keys)

    def series_stat_icon(self, name):
        stat = self.hget(name)
        map = {0: 'green', 1: 'red'}
        return url_for('static', filename='icons/bell.{}.png'.format(
            map[stat]))

    def jsonify_404(self):
        return jsonify(message=404), 404

    def help(self):
        return render_template('help.html')

    def index(self):
        return render_template('index.html')

    def series(self, name):
        return self.series_recent(name, self.default_recent)

    def series_recent(self, name, recent):
        return render_template('series.html', name=name, recent=recent)

    def series_limit(self, name, limit):
        return render_template('series.html', name=name, limit=limit)

    def series_around(self, name, around):
        num = float(self.default_recent[:-1]) / 2
        char = self.default_recent[-1]
        offset = '%.2f%s' % (num, char)
        return self.series_around_offset(name, around, offset)

    def series_around_offset(self, name, around, offset):
        if around.replace('.', '', 1).isdigit():  # numberic
            t = datetime.fromtimestamp(float(around))
        else:
            t = parse_date(around)
        timestamp = time.mktime(t.timetuple())
        return render_template('series.html', name=name, around=around,
                               offset=offset, timestamp=timestamp)

    def api_index(self):
        lst = self.hgetall()
        keys = lst[::2]
        stats = lst[1::2]
        uris = [url_for('series', name=key) for key in keys]
        items = zip(keys, stats, uris)
        return jsonify(items=items)

    def api_series_limit(self, name, limit):
        if self.hexists(name):
            if limit == 0:
                limit = -1
            series = self.zget_limit(self.zset_name(name), limit)
            return jsonify(self.make_data(series, name))
        return self.jsonify_404()

    def api_series_recent(self, name, recent):
        if self.hexists(name):
            series = self.zget_recent(self.zset_name(name), recent)
            return jsonify(self.make_data(series, name))
        return self.jsonify_404()

    def api_series_around_offset(self, name, timestamp, offset):
        half = self.parse_time_string(offset)
        t = datetime.fromtimestamp(timestamp)

        if self.hexists(name):
            start = time.mktime((t - half).timetuple())
            end = time.mktime((t + half).timetuple())
            keys = self.ssdb.zkeys(self.zset_name(name), '', start, end, -1)
            series = self.format(keys)
            return jsonify(self.make_data(series, name))
        return self.jsonify_404()

    def serve(self):
        self.initialize()
        host = configs['webapp']['host']
        port = configs['webapp']['port']
        debug = configs['webapp']['debug']
        root_path = configs['webapp']['rootPath']
        self.app.config['DEBUG'] = debug
        if not root_path:
            self.app.run(host=host, port=port)
        else:
            app = PrefixedApp(self.app, root_path)
            app.run(host, port)


webapp = WebApp()
