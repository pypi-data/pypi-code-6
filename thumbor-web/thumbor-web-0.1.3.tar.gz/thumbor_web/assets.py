#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path

from flask.ext import assets

from webassets.updater import TimestampUpdater

STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')
VENDOR_PATH = os.path.join(STATIC_PATH, 'vendor')

assets_env = assets.Environment()


def init_app(app):
    assets_env.app = app
    assets_env.init_app(app)

    assets_env.directory = app.config['ASSETS_DIRECTORY']
    cache_path = os.path.join(assets_env.directory, '.webassets_cache')
    if not app.debug and not os.path.exists(cache_path):
        os.makedirs(cache_path)
    assets_env.cache = cache_path
    assets_env.auto_build = app.config['ASSETS_AUTO_BUILD']

    assets_env.load_path = [
        os.path.join(STATIC_PATH, 'scripts'),
        os.path.join(STATIC_PATH, 'styles'),
        VENDOR_PATH
    ]

    base_libs = [
        'jquery/dist/jquery.js',
        'jquery-scrollspy/jquery-scrollspy.js',
        'jquery.breakpoints/breakpoints.js',
    ]
    js_base_bundle = assets.Bundle(*base_libs, filters=['jsmin'], output='scripts/thumbor-web.base.min.js')
    assets_env.register('js_base', js_base_bundle)

    app_files = [
        'base.coffee',
        'header.coffee',
        'breakpoints.coffee',
        'contributorsCount.coffee',
        'testimonials.coffee',
    ]
    js_app_bundle = assets.Bundle(*app_files, filters=['coffeescript', 'jsmin'], output='scripts/thumbor-web.app.min.js')
    assets_env.register('js_app', js_app_bundle)

    app.config['COMPASS_CONFIG'] = dict(
        css_dir="styles",
        sass_dir="scripts",
        images_dir="images",
        fonts_dir="fonts",
        javascripts_dir="scripts",
        relative_assets=True,
    )

    css_all_bundle = assets.Bundle(
        'all.scss',
        depends=('styles/_*.scss'),
        filters=['compass', 'cssmin'],
        output='css/thumbor-web.app.min.css'
    )
    assets_env.register('css_all', css_all_bundle)

    if app.debug:
        assets_env.set_updater(TimestampUpdater())
        assets_env.cache = False
        assets_env.auto_build = True
        assets_env.debug = True
        assets_env.manifest = "file"
