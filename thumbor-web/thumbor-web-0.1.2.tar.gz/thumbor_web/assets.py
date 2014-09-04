#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask.ext import assets

from webassets.updater import TimestampUpdater


assets_env = assets.Environment()


def init_app(app):
    assets_env.app = app
    assets_env.init_app(app)

    base_libs = [
        'vendor/jquery/dist/jquery.js',
        'vendor/jquery-scrollspy/jquery-scrollspy.js',
        'vendor/jquery.breakpoints/breakpoints.js',
    ]
    js_base_bundle = assets.Bundle(*base_libs, filters=['jsmin'], output='scripts/thumbor-web.base.min.js')
    assets_env.register('js_base', js_base_bundle)

    app_files = [
        'scripts/base.coffee',
        'scripts/header.coffee',
        'scripts/breakpoints.coffee',
        'scripts/contributorsCount.coffee',
        'scripts/testimonials.coffee',
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
        'styles/all.scss',
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
