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
:mod:`mn_deployment_ticket_generator`
=====================================

:Synopsis:
  Create tickets for tracking the progress of creating and deploying a new
  Member Node.
:Author:
  DataONE (Dahl)
:Created:
  2014-02-25
:Operation:
  The Ticket Generator is documented in the Utilities section of the
  dataone.ticket_generator package on PyPI.
'''

# Stdlib.
import datetime
import getpass
import logging
import optparse
import os
import pprint
import sys

# App.
import redmine_ticket_generator


# Create absolute path from path that is relative to the module from which
# the function is called.
def make_absolute(p):
  return os.path.join(os.path.abspath(os.path.dirname(__file__)), p)


REDMINE_URL = 'https://redmine.dataone.org/'
REDMINE_PROJECT = 'testpro'
REDMINE_VERSION = '1.3.2'
REDMINE_TRACKER = 'MNDeployment'

MN_DEPLOYMENT_TEMPLATE_PATH = make_absolute('./mn_deployment_template.yaml')


# Map custom field name to primary key. This is a workaround for not being able
# to retrieve the custom fields with redmine.custom_field.all() with the version
# of Redmine that DataONE is running as of 2014-03-13. This will work only against
# DataONE's Redmine instance.
CUSTOM_FIELD_ID_MAP = {
  'Estimatedhours': 7, # string
  'Impact': 10, # string
  'Remaining time': 14, # string
  'Risk cat': 15, # string
  'Risk prob': 16, # string
  'Totalhours': 20, # string
  'Milestone': 26, # list
  'Latitude': 27, # float
  'Longitude': 28, # float
  'MN Description': 29, # string
  'MN URL': 30, # string
  'NodeIdentifier': 31, # string
  'Product Version': 32, # string
  'MN Tier': 33, # list
  'Native data stack': 34, # string
  'OAI-PMH Stack': 35, # string
  'MN Stack': 36, # string
  'Mitigation': 37, # string
  'MN_Date_Online': 38, # date
}


def main():
  logging.basicConfig()
  logging.getLogger('').setLevel(logging.DEBUG)
  logger = logging.getLogger('main')

  usage = 'Usage: {0} <Redmine API Access Key> <Story #> <MN TAG>'.format(sys.argv[0])

  parser = optparse.OptionParser(usage=usage)

  # Redmine.

  parser.add_option('--redmine-url', dest='redmine_url', action='store',
                    type='string', default=REDMINE_URL,
                    help='URL of Redmine server')

  parser.add_option('--project', dest='redmine_project', action='store',
                    type='string', default=REDMINE_PROJECT,
                    help='Redmine project under which tickets will be created')

  parser.add_option('--tracker', dest='redmine_tracker', action='store',
                    type='string', default=REDMINE_TRACKER,
                    help='Redmine tracker to use for tickets')

  parser.add_option('--version', dest='redmine_version', action='store',
                    type='string', default=REDMINE_VERSION,
                    help='Version of Redmine server (API changes between some versions)')

  # Deployment.

  parser.add_option('--template-path', dest='ticket_template_path', action='store',
                    type='string', default=MN_DEPLOYMENT_TEMPLATE_PATH,
                    help='Path to YAML ticket template file')

  # Misc.

  parser.add_option('--verbose', action='store_true', default=False, dest='verbose')

  (options, args) = parser.parse_args()

  if len(args) != 3:
    parser.print_help()
    exit()

  try:
    story_id = int(args[1])
  except ValueError, IndexError:
    parser.print_help()
    exit()

  if options.verbose:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.INFO)

  redmine_api_access_key = args[0]
  mn_tag = args[2]

  try:
    with redmine_ticket_generator.RedmineTicketGenerator(
      redmine_url=REDMINE_URL,
      redmine_api_access_key=redmine_api_access_key,
      redmine_version=REDMINE_VERSION,
      ticket_template_str=_load(MN_DEPLOYMENT_TEMPLATE_PATH),
      template_variables_str=_generate_yaml_mn_tag(mn_tag),
      project_str=REDMINE_PROJECT,
      tracker_str=REDMINE_TRACKER,
      story_id=story_id
    ) as ticket_creator:
      ticket_creator.create_tickets()
  except redmine_ticket_generator.TicketGeneratorError as e:
    logger.error('Ticket creation failed: {0}'.format(e))
  else:
    logging.info('All tickets successfully created')


def _load(path):
  try:
    with open(path, 'rb') as f:
      return f.read()
  except IOError as e:
    raise Exception('Could not open YAML file: {0}\nError: {1}'.format(path, str(e)))


def _generate_yaml_mn_tag(mn_tag):
  return 'TitleTag: {0}'.format(mn_tag)


def _create_custom_fields(mn_description):
  return [
    #_custom_field('Estimatedhours', mn_description[]),
    #_custom_field('Impact', mn_description[]),
    #_custom_field('Remaining time', mn_description[]),
    #_custom_field('Risk cat', mn_description[]),
    #_custom_field('Risk prob', mn_description[]),
    #_custom_field('Totalhours', mn_description[]),
    #_custom_field('Milestone', mn_description[]),
    _custom_field('Latitude', mn_description['GeographicalLocation']['Latitude']),
    _custom_field('Longitude', mn_description['GeographicalLocation']['Longitude']),
    _custom_field('MN Description', mn_description['Description']),
    _custom_field('MN URL', mn_description['BaseURL']),
    _custom_field('NodeIdentifier', mn_description['NodeID']),
    #_custom_field('Product Version', mn_description[]),
    ####_custom_field('MN Tier', mn_description['Tier']),
    _custom_field('Native data stack', mn_description['Software']['NativeDataStack']),
    _custom_field('OAI-PMH Stack', mn_description['Software']['OAIPMHStack']),
    _custom_field('MN Stack', mn_description['Software']['MNStack']),
    #_custom_field('Mitigation', mn_description[]),
    #_custom_field('MN_Date_Online', mn_description[]),
  ]


def _custom_field(custom_field_name, custom_field_value):
  return {'id': CUSTOM_FIELD_ID_MAP[custom_field_name], 'value': str(custom_field_value)}


if __name__ == '__main__':
  main()
