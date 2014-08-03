from __future__ import print_function
import sys
import time
import functools

from twisted.python import usage, log
from twisted.internet import reactor, defer, endpoints
from zope.interface import implements
import txtorcon

from interface import ISubCommand
import util

_log = functools.partial(log.msg, system='carml')


class LogObserver(object):
    def __init__(self, timestamp=False, flush=True):
        self.timestamp = timestamp

    def __call__(self, arg):
        if not arg['isError'] and arg['system'] != 'carml':
            return

        msg = ' '.join(arg['message'])
        if self.timestamp:
            msg = util.colors.faint(time.asctime()) + ': ' + msg

        f = sys.stdout
        if arg['isError']:
            f = sys.stderr
        print(msg, file=f)
        if flush:
            f.flush()

log_observer = LogObserver()
log.startLoggingWithObserver(log_observer, setStdout=False)


class HelpOptions(usage.Options):
    what = None

    def parseArgs(self, what=None):
        self.what = what


class Options(usage.Options):
    """
    command-line options we understand
    """

    color_options = ['auto', 'always', 'never']

    def opt_version(self):
        "Display version and exit."
        print('carml version', __version__)
        sys.exit(0)

    ## these are all on/off
    optFlags = [
        ('timestamps', 't', 'Prepend timestamps to each line.'),
        ('no-color', 'n', 'Same as --color=no.'),
        ('quiet', 'q', 'Quiet; avoid extraneous output.'),
        ('debug', 'd', 'Debug; print stack traces on error.'),
        ]

    ## these take options, sometimes with defaults
    optParameters = [
        ('password', 'p', None, 'Password to authenticate to Tor with. Cookie-based authentication is much easier if you are on the same machine.', str),
        ('connect', 'c', 'tcp:host=127.0.0.1:port=9051', 'Where to connect to Tor. This accepts any Twisted client endpoint string, or an ip:port pair. Examples: "tcp:localhost:9151" or "unix:/var/run/tor/control".', str),
        ('color', 'C', 'auto', 'Colourize output using ANSI commands. auto, no, always', str),
        ]

    subCommands = [
        ('help', None, HelpOptions, 'Dump help on all subcommands.'),
        ]
    defaultSubCommand = 'help'

    def __init__(self):
        super(Options, self).__init__()
        self.longOpt.remove('version')

        from twisted.plugin import getPlugins
        # this is some Twisted boilerplate so we can have
        # "carml/command" for our plugin path.
        from carml import command

        # we discover any ISubCommand implementations, including the
        # built-in commands; for more about this, see:
        # http://twistedmatrix.com/documents/current/core/howto/plugin.html
        self.commands = {}
        for cmd in getPlugins(ISubCommand, command):
            self.subCommands.append((cmd.name, None, cmd.options_class, cmd.help_text))
            self.commands[cmd.name] = cmd

    def postOptions(self):
        if self['no-color']:
            self['color'] = 'never'
        if self['color'] not in self.color_options:
            print("--color accepts one of: ", ', '.join(self.color_options))
            sys.exit(2)


@defer.inlineCallbacks
def general_information(proto_or_state, verbose):
    """
    Since commands that either build or don't-build a TorState object
    both use this, we accept either.
    """

    if hasattr(proto_or_state, 'protocol'):
        proto = proto_or_state.protocol
    else:
        proto = proto_or_state
    info = yield proto.get_info('version', 'status/version/current')
    dormant = yield proto.get_info('dormant')
    if info['status/version/current'] != 'recommended' or verbose:
        sys.stderr.write('Connected to a Tor version "%(version)s" (status: %(status/version/current)s).\n' % info)
    if int(dormant['dormant']):
        msg = util.colors.red("(This Tor is dormant).\n")
        sys.stderr.write(msg)
    defer.returnValue(proto_or_state)


def setup_failed(e, debug):
    _log(util.colors.red('Error: ') + e.getErrorMessage(), isError=True)
    ## FIXME only-if debug:
    if debug:
        print(e)
    ## twisted seems to get grumpy if you do reactor.stop inside an
    ## errback
    reactor.callLater(0, reactor.stop)


def router_progress(x):
    _log('Loaded %d routers.' % x)


def dispatch(args):
    """
    this is the main program; see __main__.py
    """

    global log_observer
    options = Options()
    try:
        options.parseOptions(args[1:])

    except (usage.UsageError, RuntimeError) as e:
        _log(options.getUsage())
        _log(util.colors.red('Error: ') + str(e), isError=True)
        sys.exit(128)

    if options['color'] == 'never' or options['no-color'] or \
            (options['color'] == 'auto' and not sys.stdin.isatty()):
        util.turn_off_color()

    if options.subCommand == 'help':
        ## FIXME this is very odd, but Twisted seems to print out
        ## something different for getUsage() if invalid options have
        ## been parsed first (!!)
        ## there must be a better way ... or a Twisted patch...
        blam = Options()
        w = options.subOptions.what

        if not w:
            try:
                blam.parseOptions('foooooo')
            except:
                _log(blam.getUsage())

        else:
            sub = options.commands[w]
            desc = util.wrap(sub.help_text, 60, '    ')
            _log('Sub-command "%s":\n%s\n' % (w, desc))
            try:
                _log(options.commands[w].options_class().getUsage())

            except KeyError:
                _log('Unknown command "%s".', w)

        return 0

    else:
        sub = options.commands[options.subCommand]

        try:
            sub.validate(options.subOptions, options)
        except Exception as e:
            _log(options.getUsage())
            _log(util.colors.red('Error: ') + str(e), isError=True)
            if options['debug']:
                raise e
            return

        build_state = sub.build_state
        load_routers = sub.load_routers
        show_general_info = not options['quiet']

        endpoint = options['connect']
        try:
            endpoint = endpoints.clientFromString(reactor, options['connect'])
        except ValueError:
            try:
                endpoint = endpoints.clientFromString(reactor, 'tcp:' + options['connect'])
            except TypeError:
                endpoint = endpoints.clientFromString(reactor, 'tcp:localhost:' + options['connect'])

        if options['timestamps']:
            log_observer.timestamp = True

        if sub.controller_connection:
            d = txtorcon.build_tor_connection(endpoint,
                                              build_state=build_state,
#                                          router_progress=router_progress,
#                                          load_routers=False,##load_routers,
                                          )
        else:
            if sub.build_state:
                raise RuntimeError("Internal error: subcommand can't set build_state=True with controller_connection=False")
            d = defer.succeed(None)
            show_general_info = False

        log_observer.timestamp = options['timestamps']
        if show_general_info:
            d.addCallback(general_information, True)
        d.addCallback(functools.partial(ISubCommand(sub), options.subOptions, options))
        d.addErrback(setup_failed, options['debug'])
        return reactor.run()
