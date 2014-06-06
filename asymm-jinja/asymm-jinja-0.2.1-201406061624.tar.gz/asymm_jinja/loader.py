# -*- coding: utf-8 -*-
#    Asymmetric Base Framework :: Jinja utils
#    Copyright (C) 2013-2014 Asymmetric Ventures Inc.
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; version 2 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from __future__ import absolute_import, division, print_function, unicode_literals

from django.template import TemplateDoesNotExist
from django.template.loaders import filesystem

import jinja2

class JinjaLoader(filesystem.Loader):
	is_usable = True
	
	def __init__(self, *args, **kwargs):
		super(JinjaLoader, self).__init__(*args, **kwargs)
		try:
			from django.apps import apps
			self._env = apps.get_app_config('asymm-jinja').get_env()
		except ImportError:
			from .app_config import jinja_app
			self._env = jinja_app.get_env()
	
	def load_template(self, template_name, template_dirs = None):
		try:
			template = self._env.get_template(template_name)
			return template, template.filename
		except jinja2.TemplateNotFound:
			raise TemplateDoesNotExist(template_name)
