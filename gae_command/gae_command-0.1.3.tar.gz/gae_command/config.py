
from pkg_resources import resource_stream
import ConfigParser, os
import urllib2
from gae_command.version import __version__


headers={
	'User-Agent': 'gae_command.py/'+ __version__
}

config_file = 'gae_command.conf'
local_config_file = os.path.expanduser('~/.'+config_file)

def urlget(url):
	request = urllib2.Request(url, headers=headers)

	return urllib2.urlopen(request)

def config_read(read_local=True):
	config = ConfigParser.SafeConfigParser()
	config.optionxform = str
	if not (read_local and config.read(local_config_file)):
		rcfp = resource_stream(__name__, config_file)
		config.readfp(rcfp)
	return config

def config_save_local():
	config = config_read(read_local=False)
	local_file = open(local_config_file, 'w')
	config.write(local_file)
	local_file.close()

def get_version(url):
	"""Returns the sdk version string."""
	try:
		for line in urlget(url):
			if 'release:' in line:
				return line.split(':')[-1].strip(' \'"\r\n')
	except urllib2.URLError:
		return 'missing'

def get_remote_last_version(config=None):
	config = config or config_read()
	return get_version(config.get('globals', 'VERSION_URL'))

def get_local_version(config=None):
	config = config or config_read()
	return get_version(config.get('globals', 'VERSION_FILE'))
