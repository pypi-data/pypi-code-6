
from paste.script import templates, command, create_distro
from gae_command.config import *
import tempfile
import shutil
import os


class GAETemplate(templates.Template):

	egg_plugins = ['gae']
	summary = 'Template for creating a basic GAE package'
	_template_dir = 'templates'

	def pre(self, command, output_dir, vars):
		vars['package'] = ''
		self._template_dir = tempfile.mkdtemp()
		package_dir = os.path.join(self._template_dir, '+package+')
		config = config_read()
		local_sdk = config.get('globals', 'GAE_SDK_DIR')
		shutil.copytree(
			os.path.join(local_sdk, 'new_project_template'), package_dir)
		app_yaml = os.path.join(package_dir, 'app.yaml')
		app_yaml_txt = open(app_yaml, 'r').read()
		app_yaml_txt = app_yaml_txt.replace(
			'new-project-template', '${project}')
		open('%s_tmpl' % app_yaml, 'w').write(app_yaml_txt)
		os.unlink(app_yaml)

	def post(self, command, output_dir, vars):
		shutil.rmtree(self._template_dir)


class GAETemplateCommand(command.Command):

	summary = 'Template for creating a basic GAE package'
	parser = command.Command.standard_parser(verbose=False)

	def command(self):
		config = config_read()
		if get_local_version(config) == 'missing':
			print 'gae sdk not innstalled'
			print 'to install, run paster gae install.'
			return
		command = create_distro.CreateDistroCommand("create")
		cmd_args = []
		cmd_args.append("--template=gae")
		cmd_args.append("-q")
		command.run(cmd_args)
