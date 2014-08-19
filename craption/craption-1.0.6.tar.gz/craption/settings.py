#coding: utf-8

from configobj import ConfigObj
from craption import utils
import os
import webbrowser

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
					'path': '/srv/http/screenshots/',
					'url': 'http://example.com/screenshots&{f}'
				},
			'dropbox': {
					'token': '',
					'app': {
							'key': '',
							'secret': '',
						},
				},
		}

	conf['upload'].comments['scp'] = [
			'SSH/SFTP/SCP',
		]
	conf['upload'].comments['dropbox'] = [
                '1: Set app key and secret from https://www.dropbox.com/developers/apps'
                '2: Run craption -d'
            ]
	conf['upload']['dropbox'].comments['token'] = ['Set by craption -d']
	conf['upload'].comments['upload'] = ['Upload screenshot?']
	conf['upload'].comments['to'] = ['imgur/scp/dropbox etc']

	conf.write()

def get_conf():
    if os.path.exists(confpath):
        return ConfigObj(confpath)
    else:
        utils.install()
        print("Wrote example config to {0}".format(confpath))

def dropbox_login():
    import dropbox
    conf = get_conf()
    if not conf['upload']['dropbox']['app']['key'] or \
    not conf['upload']['dropbox']['app']['secret']:
	    conf['upload']['dropbox']['app']['key'] = raw_input("App key? ")
	    conf['upload']['dropbox']['app']['secret'] = raw_input("Secret app key? ")
    
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(
                conf['upload']['dropbox']['app']['key'],
                conf['upload']['dropbox']['app']['secret'],
	    )
    authorize_url = flow.start()
    print(authorize_url)
    webbrowser.open(authorize_url)
    code = raw_input("Authorization code: ").strip()
    access_token, user_id = flow.finish(code)

    conf['upload']['dropbox']['token'] = access_token
    conf.write()
