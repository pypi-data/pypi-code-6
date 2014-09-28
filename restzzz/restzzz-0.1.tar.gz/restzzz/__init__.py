"""Main entry point
"""
from pyramid.config import Configurator
import yaml

import restzzz.views as views

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("cornice")
    with open(config.registry.settings["restzzz.file"]) as fi:
        views.load_sockets(yaml.load(fi.read()))
    config.scan("restzzz.views")
    return config.make_wsgi_app()
