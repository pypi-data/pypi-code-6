#!/usr/bin/env python3

__authors__  = ('Ramesh (aka R4V0N3)')

__version__ = 'version 1.2.0'

import os, sys
import time
import shlex
from . import mget
from .utils import std, MGet, common, urlparse
from argparse import ArgumentParser,HelpFormatter

_TERM_WIDTH = MGet()._term_width()

def _readOptions(filename_bytes):
	res = []
	try:
		with open(filename_bytes,'r') as optionf:
			for line in optionf: res += shlex.split(line, comments=True)
	except (OSError,IOError): return res

	return res

def _readUserConf(config = True):
	userOpt = []
	config_file = os.path.join(os.path.expanduser('~'), '.config', 'mget.conf')
	if config and os.path.exists(config_file):
		userOpt = _readOptions(config_file)

	return userOpt

def _format_option_string(option):
	opts = []
	if option._short_opts: opts.append(option._short_opts[0])
	if option._long_opts: opts.append(option._long_opts[0])
	if len(opts) > 1: opts.insert(1, ', ')
	if option.takes_value(): opts.append(' %s' % option.metavar)

	return "".join(opts)

def Arguments():
	fmt = lambda prog: HelpFormatter(prog,max_help_position=40,width=_TERM_WIDTH)
	fmt.format_option_strings = _format_option_string

	usage = '\tmget [options..] URL [URL..]'
	epilog = 'Download file with ease! Send your request to r4v0n3@gmail.com.'
	args = {'usage':usage, 'prog':'mget', 'epilog':epilog,'formatter_class': fmt}
	parser = ArgumentParser(**args)

	genr = parser.add_argument_group('General arguments')
	down = parser.add_argument_group('Download arguments')
	verb = parser.add_argument_group('Simulate arguments')
	fsys = parser.add_argument_group('Filesystem arguments')

	parser.add_argument('-V', '--version', action='version', version='%(prog)s '+ __version__)

	genr.add_argument('-e', '--list-extractors', dest='extractors', action='store_true', help="Print supported Video sharing sites.")
	genr.add_argument('-I', '--ignore-errors', dest='ignore', action='store_true', help="continue on download errors, e.g. to skip unavailable videos in urlfile.")
	genr.add_argument('-m', '--mirror', dest='mirror', action='store_true', help="Download from mirror link.")
	genr.add_argument('--ignore-config', dest='ignore_config', action='store_true', help="Do not read configuration files (~/.config/mget.conf).")
	genr.add_argument('-p', dest='quitsize', metavar='PERCENT', type=float, default=100.0, help="How much percent to download default: (100.0).")
	genr.add_argument('-U', dest='useragent', metavar='USER-AGENT', type=str, help="User Agent to use.")

	down.add_argument('-T', '--timeout', dest='timeout', metavar='INT', type=int, help="set timeout values in SECONDS.")
	down.add_argument('--no-resize-buffer', dest='noresize', action='store_true', help="Do not resize the downloading buffer size.")
	down.add_argument('--retry-error', dest='retryerror', action='store_true', help="Retry on DownloadError and ContentTooShort Error's.")
	down.add_argument('--buffer', dest='buffersize', metavar='SIZE', type=int, default=1, help="Download buffer size (--buffer 3) default 1 [1024].")
	down.add_argument('--waitretry', dest='waitretry', metavar='SECONDS', type=int, default=1, help="Wait 1..SECONDS between retries of a retrieval.")
	down.add_argument('--proxy', dest='proxy', metavar='PROXY', type=str, default='', help="Use the specified HTTP/HTTPS proxy.")
#	down.add_argument('-f', dest='v_format', metavar='FORMAT', type=int, help="video format code for youtube: \"-f 18\" By default, MGet will pick the best quality.")

	verb.add_argument('-q', '--quiet', dest='quiet_mode', action='store_true', help="activates quiet mode.")
	verb.add_argument('-g', '--get-url', dest='geturl', action='store_true', help="Print Download url and exit.")
	verb.add_argument('-G', '--get-embed-url', dest='embedurl', action='store_true', help="Print embed url form the webpage, (Supported: animeram.eu, animewaffles.tv, cc-anime.com).")
	verb.add_argument('-j', '--dump-info', dest='dump_info', action='store_true', help="simulate, but print information.")
	verb.add_argument('-v', '--verbose', dest='verbose', action='store_true', help="print various debugging information.")
	verb.add_argument('--dump-user-agent', dest='dump_ua', action='store_true', help="Print User-Agent in use.")
	verb.add_argument('--dump-headers', dest='dump_headers', action='store_true', help="Print Headers recived form server.")
	verb.add_argument('--write-info', dest='write_info', action='store_true', help="simulate, and write information to 'mget_info'.")
	verb.add_argument('--newline', dest='newline', action='store_true', help="output progress bar as new lines.")
	verb.add_argument('--write-page', dest='wpage', action='store_true', help="Write downloaded pages to files in the current directory to debug.")
	verb.add_argument('--debug', dest='debug_mget', action='store_true', help="Print error debugging information.")

	fsys.add_argument('-c', '--continue', dest='continue_dl', action='store_true', help="Fource to resume download.")
	fsys.add_argument('--restart', dest='restart', action='store_true', help="Do not resume partially downloaded files (restart from beginning).")
	fsys.add_argument('--default-page', dest='def_page', metavar='PAGE', type=str, help="Change the default page name (normally this is `index.html'.).")
	fsys.add_argument('--log-file', dest='log_file', metavar='FILENAE', type=str, default='mget.log', help="Filename to write the MGet log (Default is 'mget.log').")
	fsys.add_argument('--cookies', dest='cookiefile', metavar='FILE', type=str, help="file to read cookies from and dump cookie jar in.")
	fsys.add_argument('-i', dest='urlfile', metavar='FILE', type=open, help="File with list of url to download.")
	fsys.add_argument('-O', dest='filename', metavar='FILENAME', type=str, help="File name to save the output..")

	if '--ignore-config' in sys.argv[1:]: userConf = []
	else: userConf = _readUserConf()

	argv = userConf + sys.argv[1:]
	opts, args = parser.parse_known_args(argv)

	report = []
	report.append("User config\t: %s" % userConf)
	report.append("command-line\t: %s" % ([x for x in sys.argv[1:]]))
	report.append("Encodings\t: [ %s ]" % common.pref_encoding())
	report.append("MGet\t\t: %s" % (__version__))

	if opts.verbose:
		common.write_string('\n'.join("[debug] %s" % x for x in report))
	opts.report = report
	return parser, opts, args

def check_args(opts):
	if os.name != 'posix': common._error("MGet works only on Linux!"); exit(1)
	if opts.geturl and opts.embedurl: detais_error("cannot use (-g, -G) togather"); exit(1)
	if opts.geturl and opts.dump_info: common._error("cannot use (-g, -j) togather"); exit(1)
	if opts.continue_dl and opts.restart:
		common._error("cannot use (-c, --restart) togather"); exit(1)
	if opts.extractors:
		w_sites = "\n".join('%s' % s for s in sorted(set(std.share_site_list)))
		v_sites = "\n".join('%s' % s for s in sorted(set(std.site_list)))
		common.write_string(u'// Anime websites //\n' + w_sites)
		common.write_string(u'\n// Video Sharing Sites or servers //\n' + v_sites)
		exit(1);

def main():
	if sys.version_info >= (3,4): pass
	else: common.trouble('MGet need Python (version 3.4.x) to function')
	urls = []
	parser, opts, args = Arguments()
	check_args(opts)

	info = {
	'waitretry'	: opts.waitretry,
	'cur_download'	: 0,
	'report'	: opts.report,
	'def_page'	: opts.def_page or 'index.html',
	'timeout'	: opts.timeout or 60.0,
	'user-agent'	: opts.useragent or std.UA,
	'proxy'		: opts.proxy,
	'ignore'	: opts.ignore,
#	'v_format'	: opts.v_format,
	'quit_size'	: opts.quitsize,
	'buffersize'	: opts.buffersize * 1024,
	'newline'	: opts.newline,
	'noresize'	: opts.noresize,
	'mirror'	: opts.mirror,
	'embedurl'	: opts.embedurl,
	'geturl'	: opts.geturl,
	'urlfile'	: opts.urlfile,
	'cookiefile'	: opts.cookiefile,
	'log_file'	: opts.log_file,
	'quiet_mode'	: opts.quiet_mode,
	'dump_ua'	: opts.dump_ua,
	'dump_head'	: opts.dump_headers,
	'dump_info'	: opts.dump_info,
	'write_info'	: opts.write_info,
	'wpage'		: opts.wpage,
	'continue'	: opts.continue_dl,
	'retryerror'	: opts.retryerror,
	'restart'	: opts.restart,
	'debug_mget'	: opts.debug_mget,
	'nosslcheck'	: True}

	if len(args) < 1 and not opts.urlfile: parser.print_usage()
	if opts.urlfile : urls = [x.strip() for x in opts.urlfile.readlines()]

	urls = [url.strip() for url in (urls + args)]


	for url in urls:
#		if re.match(r'', url): pass
#		else: common._error('No Url found!'); exit(1)

		info['cur_download'] += 1
		if url.startswith('-'): common._error('Option not available!'); exit(1)
		if len(url) < 2: common._error('No Url found!'); exit(1)
		opts.url = url if url.startswith('http') else "http://%s" % url
		try:
			info['defurl'] = urlparse.unquote(opts.url)
			down = mget.MGetDL(opts,info)
			down.start()
		except KeyboardInterrupt:
			common.report_error('Interrupted by user')
			exit(1)
