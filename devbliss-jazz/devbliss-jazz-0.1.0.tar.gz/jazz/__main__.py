'''
jazz

Usage:
    jazz [--port=<port>] [--debug]
    jazz (--help | --version)

Options:
    --port=<port>      http port number [default: 3000]
    --debug            enable debugging and auto-reload
    --help -h          display this help message and exit
    --version          print version information and exit

'''

import sys
import tornado.ioloop
import tornado.log
import docopt
import jazz


def main(argv=sys.argv[1:], ioloop=None):
    try:
        args = docopt.docopt(__doc__, argv=argv, version=jazz.__version__)
    except docopt.DocoptExit as e:
        print(str(e), file=sys.stderr)
        return 2
    except SystemExit as e:
        return 0
    if args.get("--debug"):
        tornado.log.enable_pretty_logging()
    application = jazz.Application(debug=args.get("--debug", False))
    application.listen(port=args.get("--port", 3000))
    try:
        (ioloop or tornado.ioloop.IOLoop.instance()).start()
    except KeyboardInterrupt:
        return 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
