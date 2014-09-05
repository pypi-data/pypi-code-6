#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from thumbor_web import handlers, config, models, assets, admin

from libthumbor import CryptoURL

app = Flask(__name__)


@app.context_processor
def utility_processor():
    def thumbor_url(image, **kw):
        image_url = "%s%s" % (app.config['SAMPLE_IMAGES_PREFIX'], image)
        encrypted_url = app.crypto.generate(
            image_url=image_url.lstrip('/'),
            **kw
        )
        return encrypted_url.lstrip('/')

    def lines_as_paragraph(text):
        lines = text.split('\n')
        result = []
        for line in lines:
            result.append('<p>%s</p>' % line)

        return "\n".join(result)

    return dict(thumbor_url=thumbor_url, lines_as_paragraph=lines_as_paragraph)


def create_app(conf_path, debug=False):
    app.debug = debug
    config.init_app(app, conf_path)

    app.crypto = CryptoURL(key=app.config['THUMBOR_SECURE_KEY'])

    logging.basicConfig(
        level=logging.DEBUG
    )

    for blueprint in (handlers, assets, models, admin):
        blueprint.init_app(app)

    if app.debug:
        app.config['DEBUG_TB_PROFILER_ENABLED'] = True
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        app.toolbar = DebugToolbarExtension(app)

    return app
