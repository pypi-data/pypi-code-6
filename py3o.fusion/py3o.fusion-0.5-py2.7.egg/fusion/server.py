from py3o.fusion.log import logging
import optparse

from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.resource import Resource
from twisted.internet import reactor

import pkg_resources

from py3o.fusion.formpage import FormPage
from py3o.fusion.indexpage import RootPage
from py3o.fusion.featurespage import FeaturesPage


def cmd_line_server():
    logging.info("py3o.fusion server starting")
    optparser = optparse.OptionParser()

    optparser.add_option(
        "-p", "--listenport",
        dest="listen_port",
        help="specify the PORT on which our service will listen",
        metavar="PORT",
        default=8765)

    optparser.add_option(
        "-s", "--renderserver",
        dest="render_server",
        help="specify the hostname/ip of the render server",
        metavar="RENDERSERVER",
        default=None)

    optparser.add_option(
        "-r", "--renderport",
        dest="render_port",
        help="specify the PORT on which the renderserver is available",
        metavar="RPORT",
        default=8994)

    (options, args) = optparser.parse_args()

    logging.info("listing on port: %s" % options.listen_port)
    start_server(options)


def start_server(options):

    reactor.suggestThreadPoolSize(30)

    root = Resource()
    root.putChild(
        "static",
        File(
            pkg_resources.resource_filename("py3o.fusion", "static")
        )
    )
    root.putChild("", RootPage())

    formpage = FormPage(options.render_server, options.render_port)

    root.putChild("form", formpage)
    root.putChild("features", FeaturesPage())
    factory = Site(root)
    reactor.listenTCP(int(options.listen_port), factory)
    reactor.run(installSignalHandlers=1)
