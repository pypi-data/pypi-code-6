import os
from django.conf import settings

class GruntRootMixin(object):
	def get_grunt_root(self):
		try:
		    return getattr(settings, 'GRUNTFILE_ROOT', settings.BASE_DIR)
		except AttributeError, e:
		    if not getattr(settings, 'GRUNTFILE_ROOT', False):
		        self.stderr.write('The GRUNTFILE_ROOT setting must not be empty')
		        self.stderr.write('Set the GRUNTFILE_ROOT setting to the directory containing Gruntfile.js')
		    else:
		        raise e
		    # Need to use an OS exit because sys.exit doesn't work in a thread
		    os._exit(1)


def create_file_from_template(filename, context={}):
	from django.template.loader import render_to_string
	with open(filename, 'wb') as f:
		f.write(render_to_string('grunt/' + filename, context))
	