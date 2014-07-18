#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
:mod:`redmine_ticket_generator`
===============================

:Synopsis:
  Create a set of Redmine tickets under a given ticket. The tickets are
  specified with a template and a set of variables that can be used in the
  template. Both the template and the variables are specified as YAML strings.
:Author:
  DataONE (Dahl)
:Created:
  2014-02-25
'''

# Stdlib.
import logging

# 3rd party.

# PyYAML. Prefer C versions if available.
import yaml
try:
  from yaml import CLoader as YAMLLoader
except ImportError:
  from yaml import Loader as YAMLLoader

# python-redmine
import redmine


log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)

class RedmineTicketGenerator():
  def __init__(self,
               redmine_url,
               redmine_api_access_key,
               redmine_version,
               ticket_template_str,
               template_variables_str,
               project_str,
               tracker_str,
               story_id
               ):
    self._redmine_url = redmine_url
    self._redmine_api_access_key = redmine_api_access_key
    self._redmine_version = redmine_version
    self._ticket_template_str = ticket_template_str
    self._template_variables_str = template_variables_str
    self._project_str = project_str
    self._tracker_str = tracker_str
    self._story_id = story_id


  def __enter__(self):
    self._redmine = self._create_redmine_client()
    self._project_id = self._get_project_id(self._project_str)
    self._tracker_id = self._get_tracker_id(self._tracker_str)
    return self


  def __exit__(self, type, value, traceback):
    pass


  def create_tickets(self):
    template_variables = self._parse_yaml(self._template_variables_str)
    ticket_template = self._parse_yaml(self._ticket_template_str)
    self._create_tickets_recursive(ticket_template, template_variables)

  #
  # Private.
  #

  def _create_tickets_recursive(self, ticket_root, template_variables, parent=None, context=None):
    '''context is a string that can be set in any level of the tree and is then
    automatically used in the ticket names for all lower levels.
    '''
    if parent is None:
      parent = self._story_id
    for ticket in ticket_root['Tasks']:
      current_context = ticket.get('Ctx', context)
      log.debug('Creating ticket. ticket={0}, env={1}'.format(ticket, current_context))
      ticket_id = self._create_ticket(parent, ticket, template_variables, current_context)
      if 'Tasks' in ticket:
        self._create_tickets_recursive(ticket, template_variables, ticket_id, current_context)


  def _create_ticket(self, parent, ticket, template_variables, context=None,
                     custom_fields=None):
    issue = self._redmine.issue.new()
    issue.project_id = self._project_id
    issue.subject = self._make_ticket_title(ticket, template_variables, context)
    issue.tracker_id = self._tracker_id
    if 'Desc' in ticket:
      issue.description = self._substitute_template_variables_variables(
        ticket['Desc'], template_variables)
    issue.parent_issue_id = parent
    #issue.status_id = 3
    #issue.priority_id = 7
    #issue.assigned_to_id = 123
    #issue.watcher_user_ids = [123]
    #issue.start_date = '2014-01-01'
    #issue.due_date = '2014-02-01'
    #issue.estimated_hours = 4
    #issue.done_ratio = 40
    if custom_fields is not None:
      issue.custom_fields = custom_fields
    issue.save()
    return issue.id


  def _make_ticket_title(self, ticket, template_variables, context):
    return template_variables['TitleTag'] + \
      ('' if not context else ' ' + context) + ': ' + \
        self._substitute_template_variables_variables(ticket['Title'], template_variables)


  def _create_redmine_client(self):
    log.debug('Creating Redmine client')
    return redmine.Redmine(self._redmine_url,
      key=self._redmine_api_access_key,
      version=self._redmine_version)


  def _get_tracker_id(self, tracker_name):
    for t in self._redmine.tracker.all():
      if t.name == tracker_name:
        return t.id
    raise TicketGeneratorError('Unknown tracker: {0}'.format(tracker_name))


  def _get_project_id(self, project_name):
    return self._redmine.project.get(project_name).id


  def _substitute_template_variables_variables(self, string, template_variables):
    return self._substitute_template_variables_variables_recursive([], string,
      template_variables)


  def _substitute_template_variables_variables_recursive(self, parent, string,
                                                     template_variables):
    for k, v in template_variables.items():
      if type(v) is dict:
        string = self._substitute_template_variables_variables_recursive(
          parent + [k], string, v)
      else:
        string = self._substitute_variable(string, '.'.join(parent + [k]), v)
    return string


  def _substitute_variable(self, string, variable, value):
    return string.replace('{{{{{0}}}}}'.format(variable), '{0}'.format(value))


  def _parse_yaml(self, yaml_string_or_stream):
    return yaml.load(yaml_string_or_stream, Loader=YAMLLoader)


class TicketGeneratorError(Exception):
  def __init__(self, value):
    self.value = value


  def __str__(self):
    return str(self.value)
