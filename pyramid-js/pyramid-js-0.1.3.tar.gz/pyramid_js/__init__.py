__version__ = '0.1.3'

import os
import re
import json
import textwrap

from markupsafe import Markup
from pyramid.events import ApplicationCreated
from pyramid.asset import abspath_from_asset_spec

here = os.path.abspath(os.path.dirname(__file__))

_argument_prog = re.compile('\{(.*?)\}')


def __replace(matchobj):
    if matchobj.group(1):
        return "%%(%s)s" % matchobj.group(1).split(':')[0]
    else:
        return "%%(%s)s" % matchobj.group(2)


def generate_json_routes(introspector):
    result = {}

    for r in introspector.get_category('routes'):
        pattern = '/%s' % r['introspectable']['pattern'].lstrip('/')
        result[r['introspectable']['name']] = (
            _argument_prog.sub(__replace, pattern),
            [
                arg.split(':')[0] for arg in _argument_prog.findall(pattern)
            ]
        )

    return json.dumps(result)


def generate_pyramid_js_file(registry):
    src = open(os.path.join(here, 'pyramid.js'), 'r')
    pyramid_js = src.read()
    src.close()

    f = open(registry.settings.get('pyramid_js.file'), 'w')
    f.write(
        pyramid_js % {
            'json': generate_json_routes(registry.introspector)
        }
    )
    f.close()


def __application_created(event):
    generate_pyramid_js_file(event.app.registry)


class PyramidJS(object):
    def __init__(self, settings=None):
        if settings:
            self.settings = settings
        else:
            self.settings = {}

    def javascript(self, settings=None):
        if settings is None:
            settings = {}

        settings.update(self.settings)

        return (textwrap.dedent(Markup(
            """
            var pyramid = PyramidJS(%s);
            """ % json.dumps(settings)
        )))


def _pyramidjs(request):
    p = PyramidJS(settings={
        'host': request.host,
        'host_url': request.host_url,
        'path': request.path,
        'url': request.url,
        'path_url': request.path_url,
        'path_qs': request.path_qs,
        'query_string': request.query_string
    })
    return p


def includeme(config):
    config.add_subscriber(__application_created, ApplicationCreated)
    config.set_request_property(_pyramidjs, 'pyramidjs', reify=False)
