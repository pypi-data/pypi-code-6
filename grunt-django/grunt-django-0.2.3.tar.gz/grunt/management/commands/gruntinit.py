from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
from os import path
import subprocess
from grunt.utils import GruntRootMixin, create_file_from_template


class Command(BaseCommand,GruntRootMixin):
	help = 'Initialize you project for using GRUNT'
	project_name = None

	def handle(self, *args, **options):
		self.get_project_name()
		package_json_created = self.create_package_file()

		if package_json_created or not path.exists(path.join(self.get_grunt_root(), 'node_modules') ):
			self.npm_install()

		self.create_gruntfile()

	def create_gruntfile(self):
		grunt_root = self.get_grunt_root() 
		create_gruntfile = True
		if os.path.exists(os.path.join(grunt_root, 'Gruntfile.js')):
			create_gruntfile = self.get_boolean_input_data('Overwrite Gruntfile.js')

		if create_gruntfile:
			try:
				static_root = settings.STATIC_ROOT
				if not static_root:
					raise Exception
			except:
				default_static_root = "%s/static"%self.get_project_name()
				static_root = self.get_input_data(
					message="Select static root (default : %s)"%default_static_root,
					default=default_static_root
				)

			create_file_from_template('Gruntfile.js',{'static_root': static_root})
			self.stdout.write("Gruntfile.js CREATED!")


	def npm_install(self):
		#run npm install
		try:
			subprocess.call(['npm', 'install'])
		except:
			self.stderr.write("I can't execute npm install.")
			self.stderr.write("Please check that node.js and npm are installed on your system.")
			self.stderr.write("If node.js is not installed, please visit http://nodejs.org/download/")
			os._exit(1)




	def create_package_file(self):
		grunt_root = self.get_grunt_root() 
		#Check if package.json file already exists 
		create_package_json = True
		if os.path.exists(os.path.join(grunt_root, 'package.json')):
			create_package_json = self.get_boolean_input_data('Overwrite package.json')

		if create_package_json:
			create_file_from_template('package.json',{'project_name': self.get_project_name()})
			self.stdout.write("package.json CREATED!")

		return create_package_json


	def get_project_name(self):
		if not self.project_name:
			try:
				project_name_default = os.path.split(settings.BASE_DIR)[1]
			except:
				project_name_default = None

			if project_name_default:
				message = "Type your project name (default '%s'): "%project_name_default
				project_name = self.get_input_data(message, project_name_default)

			else:
				project_name == ''
				message = "Type your project name: "
				while not project_name:
					project_name = self.get_input_data(project_name)

			self.project_name = project_name

		return self.project_name 



	def get_input_data(self, message, default=None):
		"""
		Override this method if you want to customize data inputs or
		validation exceptions.
		"""
		raw_value = raw_input(message)
		if default and raw_value == '':
			raw_value = default

		return raw_value

	def get_boolean_input_data(self, message):
		"""
		Override this method if you want to customize data inputs or
		validation exceptions.
		"""
		raw_value = None
		while raw_value != 'y' and raw_value != 'n':
			raw_value = raw_input(message + '(y/n)? ')

		return raw_value == 'y'
		
	   
