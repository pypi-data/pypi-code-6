#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pedro Tome <Pedro.Tome@idiap.ch>
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

  def add_file(session, subdir, filename, client_dict, verbose):
    """Parse a single filename and add it to the list.
       Also add a client entry if not already in the database."""

    v = os.path.splitext(os.path.basename(filename))[0].split('_')
    subclient_id = int(v[0])
    finger_id = int(v[1])
    ### 1 = Left ring finger
    ### 2 = Left middle finger
    ### 3 = Left index finger
    ### 4 = Right index finger
    ### 5 = Right middle finger
    ### 6 = Right ring finger
    client_id = "%d_%d" % (subclient_id, finger_id)
    if not (client_id in client_dict):
      c = Client(client_id, subclient_id)
      session.add(c)
      session.flush()
      session.refresh(c)
      client_dict[client_id] = True
    session_id = int(v[2])
    base_path = os.path.join(subdir, os.path.basename(filename).split('.')[0])
    if verbose>1: print("  Adding file '%s'..." %(base_path, ))
    cfile = File(client_id, base_path, finger_id, session_id)
    session.add(cfile)
    session.flush()
    session.refresh(cfile)

    return cfile
  
  if verbose: print("Adding files...")
  subdir_list = list(filter(nodot, os.listdir(imagedir)))
  client_dict = {}
  file_list = []
  for subdir in subdir_list:
    filename_list = list(filter(nodot, os.listdir(os.path.join(imagedir, subdir))))
    for filename in filename_list:
      filename_, extension = os.path.splitext(filename)
      if extension == '.png':
        file_list.append(add_file(session, subdir, os.path.join(imagedir, filename), client_dict, verbose))

  return file_list

def add_protocols(session, file_list, verbose):
  """Adds protocols"""
    
  # 2. ADDITIONS TO THE SQL DATABASE
  protocol_list = ['1vsall', 'nom','nomLeftRing','nomLeftMiddle','nomLeftIndex','nomRightIndex','nomRightMiddle','nomRightRing']
  for proto in protocol_list:
    p = Protocol(proto)
    # Add protocol
    if verbose: print("Adding protocol %s..." % (proto))
    session.add(p)
    session.flush()
    session.refresh(p)
    
    if proto == '1vsall':
      # Helper function
      def isWorldFile(f_file):
        return f_file.client.subclient_id <= 35 and f_file.finger_id == ((f_file.client.subclient_id-1) % 6) + 1

      model_dict = {}
      for f_file in file_list:      
        if not isWorldFile(f_file):
          model_id = "%s_%d" % (f_file.client_id, f_file.session_id)
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            model = Model(model_id, f_file.client_id, 'dev')
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            # Append probe files
            for f_pfile in file_list:
              if f_pfile.id != f_file.id and not isWorldFile(f_pfile):
                model.probe_files.append(f_pfile)
                if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))
            model_dict[model_id] = model
          # Append enrollment file
          model_dict[model_id].enrollment_files.append(f_file)
          if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev', 'enrol'))
          session.flush()
          
        else:
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))
      
      
    if proto == 'nom':
      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id <= 2)
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id > 2)
                
      def isEvalEnrollFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id <= 2)
      def isEvalProbeFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id > 2)
        
      model_dict = {}
      for f_file in file_list:
        model_id = f_file.client_id
        if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):          
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

            if isEvalEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isEvalProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'eval', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enrol'))
             
        elif f_file.client.subclient_id <= 10:
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))   

         
    if proto == 'nomLeftRing':
         
      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id <= 2 and f_file.finger_id == 1)
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id > 2 and f_file.finger_id == 1)
                
      def isEvalEnrollFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id <= 2 and f_file.finger_id == 1)
      def isEvalProbeFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id > 2 and f_file.finger_id == 1)
        
      model_dict = {}
      for f_file in file_list:
        model_id = f_file.client_id
        #import ipdb; ipdb.set_trace()    
        if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):          
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

            if isEvalEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isEvalProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'eval', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enrol'))
             
        elif f_file.client.subclient_id <= 10 and f_file.finger_id == 1:
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))

    if proto == 'nomLeftMiddle':
         
      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id <= 2 and f_file.finger_id == 2)
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id > 2 and f_file.finger_id == 2)
                
      def isEvalEnrollFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id <= 2 and f_file.finger_id == 2)
      def isEvalProbeFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id > 2 and f_file.finger_id == 2)
        
      model_dict = {}
      for f_file in file_list:
        model_id = f_file.client_id
        if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):          
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

            if isEvalEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isEvalProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'eval', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enrol'))
             
        elif f_file.client.subclient_id <= 10 and f_file.finger_id == 2:
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))

    if proto == 'nomLeftIndex':
         
      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id <= 2 and f_file.finger_id == 3)
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id > 2 and f_file.finger_id == 3)
                
      def isEvalEnrollFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id <= 2 and f_file.finger_id == 3)
      def isEvalProbeFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id > 2 and f_file.finger_id == 3)
        
      model_dict = {}
      for f_file in file_list:
        model_id = f_file.client_id
        if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):          
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

            if isEvalEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isEvalProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'eval', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enrol'))
             
        elif f_file.client.subclient_id <= 10 and f_file.finger_id == 3:
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))   

    if proto == 'nomRightIndex':
         
      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id <= 2 and f_file.finger_id == 4)
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id > 2 and f_file.finger_id == 4)
                
      def isEvalEnrollFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id <= 2 and f_file.finger_id == 4)
      def isEvalProbeFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id > 2 and f_file.finger_id == 4)
        
      model_dict = {}
      for f_file in file_list:
        model_id = f_file.client_id
        if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):          
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

            if isEvalEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isEvalProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'eval', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enrol'))
             
        elif f_file.client.subclient_id <= 10 and f_file.finger_id == 4:
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))                
             

    if proto == 'nomRightMiddle':
         
      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id <= 2 and f_file.finger_id == 5)
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id > 2 and f_file.finger_id == 5)
                
      def isEvalEnrollFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id <= 2 and f_file.finger_id == 5)
      def isEvalProbeFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id > 2 and f_file.finger_id == 5)
        
      model_dict = {}
      for f_file in file_list:
        model_id = f_file.client_id
        if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):          
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

            if isEvalEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isEvalProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'eval', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enrol'))
             
        elif f_file.client.subclient_id <= 10 and f_file.finger_id == 5:
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))       


    if proto == 'nomRightRing':
         
      # Helper functions
      def isDevEnrollFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id <= 2 and f_file.finger_id == 6)
      def isDevProbeFile(f_file):
        return (f_file.client.subclient_id >= 11 and f_file.client.subclient_id <= 28 and f_file.session_id > 2 and f_file.finger_id == 6)
                
      def isEvalEnrollFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id <= 2 and f_file.finger_id == 6)
      def isEvalProbeFile(f_file):
        return (f_file.client.subclient_id >= 29 and f_file.session_id > 2 and f_file.finger_id == 6)
        
      model_dict = {}
      for f_file in file_list:
        model_id = f_file.client_id
        if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):          
          if verbose>1: print("  Adding Model '%s'..." %(model_id, ))
          if not model_id in model_dict:
            sgroup = 'dev' if isDevEnrollFile(f_file) else 'eval'
            model = Model(model_id, f_file.client_id, sgroup)
            p.models.append(model)
            session.add(model)
            session.flush()
            session.refresh(model)
            model_dict[model_id] = model

            if isDevEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isDevProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'dev', 'probe'))

            if isEvalEnrollFile(f_file):
              # Append probe files
              for f_pfile in file_list:
                if isEvalProbeFile(f_pfile):
                  model_dict[model_id].probe_files.append(f_pfile)
                  if verbose>1: print("   Adding probe entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_pfile.path, model_id, p.name, 'eval', 'probe'))

          # It is an enrollment file: append it
          if isDevEnrollFile(f_file) or isEvalEnrollFile(f_file):
            model_dict[model_id].enrollment_files.append(f_file)
            if verbose>1: print("   Adding enrollment entry ('%s') to Model ('%s') for protocol purpose ('%s', '%s','%s')..." % (f_file.path, model_id, p.name, 'dev' if isDevEnrollFile(f_file) else 'eval', 'enrol'))
             
        elif f_file.client.subclient_id <= 10 and f_file.finger_id == 6:
          p.train_files.append(f_file)
          if verbose>1: print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, 'world', 'train'))        


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
  file_list = add_files(s, args.imagedir, args.verbose)
  add_protocols(s, file_list, args.verbose)
  s.commit()
  s.close()

def add_command(subparsers):
  """Add specific subcommands that the action "create" can use"""

  parser = subparsers.add_parser('create', help=create.__doc__)

  parser.add_argument('-R', '--recreate', action='store_true', help="If set, I'll first erase the current database")
  parser.add_argument('-v', '--verbose', action='count', help='Do SQL operations in a verbose way')
  parser.add_argument('-D', '--imagedir', metavar='DIR', default='/idiap/resource/database/UTFVP/data', help="Change the relative path to the directory containing the images of the UTFVP database (defaults to %(default)s)")

  parser.set_defaults(func=create) #action
