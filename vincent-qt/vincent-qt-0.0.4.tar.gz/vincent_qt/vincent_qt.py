#!/usr/bin/python3
"""Visualizer of vega graphs"""

try:
    from PyQt5.QtCore import QUrl
    from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkDiskCache, QNetworkRequest
except ImportError:
    try:
        from PyQt4.QtCore import QUrl
        from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkDiskCache, QNetworkRequest
    except ImportError:
        raise ImportError("Cannot import PyQt4 or PyQt5!")

try:
    import appdirs
    cache_dir = appdirs.user_cache_dir('vincent-qt')
except ImportError:
    cache_dir = '.vincent-qt_cache'


import tempfile
import string
import os
import atexit
import os.path


class CachingNetworkAccessManager(QNetworkAccessManager):
    def __init__(self, parent=None, caching=QNetworkRequest.AlwaysCache):
        super().__init__(parent)
        self._caching = caching

    def createRequest(self, op, req, outgoingData=0):
        request = QNetworkRequest(req)
        request.setAttribute(QNetworkRequest.CacheLoadControlAttribute, self._caching)
        return super().createRequest(op, request, outgoingData)


def enable_caching(web_view, caching=QNetworkRequest.AlwaysCache):
    network_access_manager = CachingNetworkAccessManager(web_view, caching)
    disk_cache = QNetworkDiskCache(web_view)
    disk_cache.setCacheDirectory(cache_dir)
    network_access_manager.setCache(disk_cache)
    web_view.page().setNetworkAccessManager(network_access_manager)


def display(web_view, plot, fit_into_web_view=True, caching=QNetworkRequest.AlwaysCache):
    if fit_into_web_view:
        ### BUG: there should be no magic! (I didn't find how to find full rect correctly)
        ### BUG: it's not good way to resize
        magic_coefficient = 0.9
        plot.width = int(magic_coefficient*web_view.width())
        plot.height = int(magic_coefficient*web_view.height())
    if caching > QNetworkRequest.AlwaysNetwork:
        if caching == QNetworkRequest.AlwaysCache and not os.path.exists(cache_dir):
            caching = QNetworkRequest.PreferNetwork
        enable_caching(web_view, caching)

    json_plot_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    json_plot_file.write(plot.to_json())
    json_plot_file.close()
    template = string.Template("""
        <html>
          <head>
            <style>
              body{ background-color: #FFFFFF; }
            </style>
            <script src="http://trifacta.github.io/vega/lib/d3.v3.min.js"></script>
            <script src="http://trifacta.github.io/vega/lib/d3.geo.projection.min.js"></script>
            <script src="http://trifacta.github.io/vega/lib/topojson.js"></script>
            <script src="http://trifacta.github.io/vega/vega.js"></script>
          </head>
          <body>
            <div style="text-align: center; vertical-align: middle" id="vis"></div>
          </body>
            <script type="text/javascript">
            // parse a spec and create a visualization view
            function parse(spec) {
              vg.parse.spec(spec, function(chart) { chart({el:"#vis"}).update(); });
            }
            parse("file://$json_filename");
          </script>
        </html>
    """).substitute(json_filename=json_plot_file.name)
    template_file = tempfile.NamedTemporaryFile('w', suffix='.html', delete=False)
    template_file.write(template)
    template_file.close()
    template_url = QUrl.fromLocalFile(template_file.name)
    web_view.setUrl(template_url)

    def remove_files():
        os.remove(template_file.name)
        os.remove(json_plot_file.name)

    atexit.register(remove_files)
