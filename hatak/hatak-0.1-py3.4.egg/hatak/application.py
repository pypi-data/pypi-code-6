import logging

from pyramid.config import Configurator
from smallsettings import Factory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Application(object):

    """Prepering and configuring project."""

    def __init__(self, module, make_routes):
        self.make_routes = make_routes
        self.module = module

    def __call__(self, settings={}):
        self.settings = self.generate_settings(settings)
        self.initialize_logging()
        self.create_config()
        self.connect_database()
        self.config.include('pyramid_jinja2')
        self.config.registry['settings'] = self.settings
        self.config.registry['jinja2'] = self.config.get_jinja2_environment()

        return self.config.make_wsgi_app()

    def generate_settings(self, settings):
        settings, paths = self.get_settings(self.module, settings)
        merged = settings.merged(paths)
        return merged.to_dict()

    @classmethod
    def get_settings(cls, module, settings={}):
        factory = Factory('%s.application' % (module))
        settings, paths = factory.make_settings(
            settings=settings,
            additional_modules=[
                ('local', False),
            ])
        return settings, paths

    def initialize_logging(self):
        logging.config.fileConfig(
            self.settings['logging:config'],
            disable_existing_loggers=False)

    def create_config(self):
        self.config = Configurator(
            settings=self.settings,
        )
        self.make_pyramid_includes()
        self.make_routes(self)

    def connect_database(self):
        engine = create_engine(self.settings['db:url'])
        self.config.registry['db'] = sessionmaker(bind=engine)()
        self.config.registry['db_engine'] = engine

    def make_pyramid_includes(self):
        for include in self.settings['includes']:
            self.config.include(include)
