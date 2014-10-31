#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
#
# Copyright (C) 2014 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""This script creates the UTFVP database in a single pass.
"""

import os

from .models import *

def nodot(item):
  """Can be used to ignore hidden files, starting with the . character."""
  return item[0] != '.'

def add_files(session, imagedir, verbose):
  """Add files (and clients) to the UTFVP database."""

  def add_file(session, subdir, filename, client_dict, model_dict, file_dict, verbose):
    """Parse a single filename and add it to the list.
       Also add a client entry if not already in the database."""

    v = os.path.splitext(os.path.basename(filename))[0].split('_')
    subclient_id = int(v[0])
    finger_id = int(v[1])
    client_id = "%d_%d" % (subclient_id, finger_id)
    if not (client_id in client_dict):
      c = Client(client_id, subclient_id)
      session.add(c)
      session.flush()
      session.refresh(c)
      client_dict[client_id] = True
    session_id = int(v[2])
    base_path = os.path.join(subdir, os.path.basename(filename).split('.')[0])
    sgroup = 'dev'
    if subclient_id <= 36:
      if subclient_id < 19:
        if finger_id == ((subclient_id-1) % 6) + 1:
          sgroup = 'world'
      elif subclient_id > 19:
        if finger_id == ((subclient_id-2) % 6) + 1:
          sgroup = 'world'
    if verbose>1: print("  Adding file '%s'..." %(base_path, ))
    cfile = File(client_id, base_path, sgroup, finger_id, session_id)
    session.add(cfile)
    session.flush()
    session.refresh(cfile)
    file_dict[sgroup][cfile.id] = cfile
    if sgroup == 'dev':
      model_id = "%d_%d_%d" % (subclient_id, finger_id, session_id)
      if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
      model = Model(model_id, client_id, cfile.id)
      session.add(model)
      session.flush()
      session.refresh(model)
      model_dict[model_id] = model
    return [client_dict, model_dict, file_dict]

  if verbose: print("Adding files...")
  subdir_list = list(filter(nodot, os.listdir(imagedir)))
  client_dict = {}
  model_dict = {}
  file_dict = {}
  file_dict['world'] = {}
  file_dict['dev'] = {}
  for subdir in subdir_list:
    file_list = list(filter(nodot, os.listdir(os.path.join(imagedir, subdir))))
    for filename in file_list:
      filename_, extension = os.path.splitext(filename)
      if extension == '.png':
        client_dict, model_dict, file_dict = add_file(session, subdir, os.path.join(imagedir, filename), client_dict, model_dict, file_dict, verbose)

  return [client_dict, model_dict, file_dict]

def add_protocols(session, client_dict, model_dict, file_dict, verbose):
  """Adds protocols"""
  # 2. ADDITIONS TO THE SQL DATABASE
  protocol_list = ['master', 'paper', 'B']
  protocolPurpose_list = [('world', 'train'), ('dev', 'enrol'), ('dev', 'probe')]
  for proto in protocol_list:
    p = Protocol(proto)
    # Add protocol
    if verbose: print("Adding protocol %s..." % (proto))
    session.add(p)
    session.flush()
    session.refresh(p)
   
    for purpose in protocolPurpose_list:
      pu = ProtocolPurpose(p.id, purpose[0], purpose[1])
      if verbose>1: print(" Adding protocol purpose ('%s', '%s','%s')..." % (p.name, purpose[0], purpose[1]))
      session.add(pu)
      session.flush()
      session.refresh(pu)

      cfile_dict = file_dict[purpose[0]]
      for f_id, f_file in cfile_dict.iteritems():
        if f_file.client.subclient_id == 19 and proto == 'master':
          continue
        if not ((f_file.finger_id == 3 or f_file.finger_id == 4) and (f_file.session_id == 1 or f_file.session_id == 2)) and proto == 'B':
          continue
        if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, purpose[0], purpose[1]))
        pu.files.append(f_file)
    
    for m_id, model in model_dict.iteritems():
      if model.client.subclient_id == 19 and proto == 'master':
        continue
      if not ((model.file.finger_id == 3 or model.file.finger_id == 4) and (model.file.session_id == 1 or model.file.session_id == 2)) and proto == 'B':
        continue
      p.models.append(model)


def create_tables(args):
  """Creates all necessary tables (only to be used at the first time)"""

  from bob.db.utils import create_engine_try_nolock

  engine = create_engine_try_nolock(args.type, args.files[0], echo=(args.verbose > 2))
  Base.metadata.create_all(engine)

# Driver API
# ==========

def create(args):
  """Creates or re-creates this database"""

  from bob.db.utils import session_try_nolock

  dbfile = args.files[0]

  if args.recreate:
    if args.verbose and os.path.exists(dbfile):
      print('unlinking %s...' % dbfile)
    if os.path.exists(dbfile): os.unlink(dbfile)

  if not os.path.exists(os.path.dirname(dbfile)):
    os.makedirs(os.path.dirname(dbfile))

  # the real work...
  create_tables(args)
  s = session_try_nolock(args.type, args.files[0], echo=(args.verbose > 2))
  client_dict, model_dict, file_dict = add_files(s, args.imagedir, args.verbose)
  add_protocols(s, client_dict, model_dict, file_dict, args.verbose)
  s.commit()
  s.close()

def add_command(subparsers):
  """Add specific subcommands that the action "create" can use"""

  parser = subparsers.add_parser('create', help=create.__doc__)

  parser.add_argument('-R', '--recreate', action='store_true', help="If set, I'll first erase the current database")
  parser.add_argument('-v', '--verbose', action='count', help='Do SQL operations in a verbose way')
  parser.add_argument('-D', '--imagedir', metavar='DIR', default='/idiap/resource/database/UTFVP/data', help="Change the relative path to the directory containing the images of the UTFVP database (defaults to %(default)s)")

  parser.set_defaults(func=create) #action
