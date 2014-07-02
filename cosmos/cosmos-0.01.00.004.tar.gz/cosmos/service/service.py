from cosmos.service import auth, servicehandler
import settings

__author__ = 'Maruf Maniruzzaman'

import tornado.ioloop
import tornado.web
import tornado.options
import tornado.template
import tornado.websocket
from cosmos.dataservice.objectservice import *
from cosmos.comet.monitor import *

application = None

def start_web_service(db, port, endpoints, login_url):
    global application
    application = tornado.web.Application(
        endpoints,
        db=db,
        login_url= login_url,
        cookie_secret=settings.COOKIE_SECRET,
        xheaders=True,
        template_path=settings.TEMPLATE_PATH,
        debug=settings.DEBUG
    )

    logging.info('Starting up server on port: {0}'.format(port))
    application.listen(port)
