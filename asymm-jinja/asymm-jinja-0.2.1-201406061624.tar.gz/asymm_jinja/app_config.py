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

import django
from django.conf import settings
from django.utils import html as django_html_utils
import jinja2
from markupsafe import Markup

try:
	from django.apps import AppConfig
except ImportError:
	AppConfig = object

class JinjaAppConfig(AppConfig):
	name = 'asymm_jinja'
	
	def __init__(self, *args, **kwargs):
		super(JinjaAppConfig, self).__init__(*args, **kwargs)
		self._env = None
	
	def ready(self):
		self.patch_conditional_escape()
	
	def patch_conditional_escape(self):
		"""
		Override django's conditional_escape to look for jinja's MarkupSafe
		"""
		old_conditional_escape = django_html_utils.conditional_escape
		
		conditional_escape = lambda html: html if isinstance(html, Markup) else old_conditional_escape(html)
		
		setattr(django_html_utils, 'conditional_escape', conditional_escape)
	
	def get_env(self):
		if self._env is None:
			from django.template.loaders.app_directories import app_template_dirs
			from jinja2.ext import WithExtension, LoopControlExtension
			from . import environment, filters, global_functions
			from .tags import csrf_token
			
			template_loader = getattr(settings, 'ASYM_TEMPLATE_LOADER', jinja2.FileSystemLoader(app_template_dirs))
			
			if callable(template_loader):
				template_loader = template_loader()
			
			self._env = environment.JinjaEnvironment(
				loader = template_loader,
				undefined = environment.UndefinedVar,
				autoescape = True,
				extensions = [
					csrf_token.CSRFTokenExtension,
					WithExtension,
					LoopControlExtension
				]
			)
			
			self._env.filters.update(filters.get_filters(self._env))
			self._env.globals.update(global_functions.get_functions(self._env))
			
		return self._env

if django.get_version() < '1.7':
	jinja_app = JinjaAppConfig()
	jinja_app.ready()
