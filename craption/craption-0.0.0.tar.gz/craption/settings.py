#coding: utf-8

from configobj import ConfigObj
from craption import utils
import os

home = os.getenv('USERPROFILE') or os.getenv('HOME')
confpath = "%s/%s" % (home, '.craptionrc')
noise_path = "%s/%s" % (home, '.craption_noise.wav')

def write_template():
	conf = ConfigObj(
			confpath,
			create_empty = True,
			indent_type = "	",
			write_empty_values = True,
		)
	
	conf['file'] = {
			'name': 'CRAPtion_{r5}_{u}_{d}',
			'dir': '~/craptions',
			'keep': True,
			'datetime_format': '%Y-%m-%d',
		}

	conf['file'].comments['name'] = [
			"Filename",
			"{rx}	x random chars",
			"{u}	Unix timestamp",
			"{d}	Datetime",
		]
	conf['file'].comments['dir'] = ['Local screenshot directory']
	conf['file'].comments['keep'] = ['Save screenshots to local path']
	conf['file'].comments['datetime_format'] = ['http://docs.python.org/library/datetime.html#strftime-and-strptime-behavior']

	conf['upload'] = {
			'upload': True,
			'to': 'imgur',
			'imgur': {
					'api-key': 'd4ce1fd7b955cddf8a9a179f3c9bee47',
				},
			'scp': {
					'user': 'myuser',
					'host': 'example.com',
					'path': '/srv/http/something/whatever',
					'url': 'http://example.com/{f}'
				},
			'dropbox': {
					'app': {
							'key': '',
							'secret': '',
						},
					'token': {
							'key': '',
							'secret': '',
						},
				},
		}

	conf['upload'].comments['scp'] = [
			'SSH/SFTP/SCP',
			'http://dwight.schrute.org/ssh-login-without-password-using-ssh-keys',
		]
	conf['upload'].comments['dropbox'] = [
			'Run settings.py dropbox to log in, get keys from',
			'https://www.dropbox.com/developers/apps'
		]
	conf['upload'].comments['upload'] = ['Upload screenshot?']
	conf['upload'].comments['to'] = ['imgur/scp/dropbox etc']

	conf.write()

def get_conf():
    if os.path.exists(confpath):
        return ConfigObj(confpath)
    else:
        utils.install()
        print("Wrote example config to {0}".format(confpath))

#def dropbox_login():
#        import dropbox
#	url = "https://api.dropbox.com/1/oauth/request_token"
#	conf = get_conf()
#	if not conf['upload']['dropbox']['app']['key'] or \
#	not conf['upload']['dropbox']['app']['secret']:
#		conf['upload']['dropbox']['app']['key'] = raw_input("App key? ")
#		conf['upload']['dropbox']['app']['secret'] = raw_input("Secret app key? ")
#	
#	sess = dropbox.session.DropboxSession(
#			conf['upload']['dropbox']['app']['key'],
#			conf['upload']['dropbox']['app']['secret'],
#			'app_folder'
#		)
#
#	request_token = sess.obtain_request_token()
#	print sess.build_authorize_url(request_token)
#	raw_input("Press any key to continue...")
#	token = sess.obtain_access_token(request_token)
#	conf['upload']['dropbox']['token']['key'] = token.key
#	conf['upload']['dropbox']['token']['secret'] = token.secret
#	conf.write()
