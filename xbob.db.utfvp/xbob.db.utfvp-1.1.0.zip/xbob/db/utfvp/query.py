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

"""This module provides the Dataset interface allowing the user to query the
UTFVP database in the most obvious ways.
"""

import os
import six
from bob.db import utils
from .models import *
from .driver import Interface

import xbob.db.verification.utils

SQLITE_FILE = Interface().files()[0]

class Database(xbob.db.verification.utils.SQLiteDatabase):
  """The dataset class opens and maintains a connection opened to the Database.

  It provides many different ways to probe for the characteristics of the data
  and for the data itself inside the database.
  """

  def __init__(self, original_directory = None, original_extension = None):
    # call base class constructors
    xbob.db.verification.utils.SQLiteDatabase.__init__(self, SQLITE_FILE, File)

  def groups(self, protocol=None):
    """Returns the names of all registered groups"""

    return File.group_choices

  def clients(self, protocol=None, groups=None):
    """Returns a set of clients for the specific query by the user.

    Keyword Parameters:

    protocol
      One of the UTFVP protocols ('master', 'paper').

    groups
      ignored (The clients belong both to 'world' and 'dev')

    Returns: A list containing all the clients which have the given properties.
    """

    protocols = self.check_parameters_for_validity(protocol, "protocol", self.protocol_names())

    retval = []
    # List of the clients
    q = self.query(Client)
    if len(protocols) == 1 and protocols[0] == 'master':
      q = q.filter(not_(Client.id.in_(('19_1', '19_2', '19_3', '19_4', '19_5', '19_6'))))
    q = q.order_by(Client.id)
    retval += list(q)

    return retval

  def client_ids(self, protocol=None, groups=None):
    """Returns a set of client ids for the specific query by the user.

    Keyword Parameters:

    protocol
      One of the UTFVP protocols ('master', 'paper').

    groups
      ignored (The clients belong both to 'world' and 'dev')

    Returns: A list containing all the clients which have the given properties.
    """

    return [client.id for client in self.clients(protocol, groups)]

  def models(self, protocol=None, groups=None):
    """Returns a set of models for the specific query by the user.

    Keyword Parameters:

    protocol
      One of the UTFVP protocols ('master', 'paper').

    groups
      Returns models from the 'dev' if None or 'dev' are given.
      Nothing otherwise

    Returns: A list containing all the models which have the given properties.
    """

    protocols = self.check_parameters_for_validity(protocol, "protocol", self.protocol_names())
    groups = self.check_parameters_for_validity(groups, "group", self.groups())

    retval = []
    if 'dev' in groups:
      # List of the clients
      q = self.query(Model).join((Protocol, Model.protocols)).filter(Protocol.name.in_(protocols))
      q = q.order_by(Model.name)
      retval += list(q)

    return retval

  def model_ids(self, protocol=None, groups=None):
    """Returns a set of models ids for the specific query by the user.

    Keyword Parameters:

    protocol
      Two possible protocols: 'paper' or 'master'

    groups
      The groups to which the subjects attached to the models belong ('dev')

    Returns: A list containing all the models ids which have the given properties.
    """

    return [model.name for model in self.models(protocol, groups)]

  def has_client_id(self, id):
    """Returns True if we have a client with a certain integer identifier"""

    return self.query(Client).filter(Client.id==id).count() != 0

  def client(self, id):
    """Returns the client object in the database given a certain id. Raises
    an error if that does not exist."""

    return self.query(Client).filter(Client.id==id).one()

  def get_client_id_from_model_id(self, model_id):
    """Returns the client_id attached to the given model_id

    Keyword Parameters:

    model_id
      The model_id to consider

    Returns: The client_id attached to the given model_id
    """
 
    return self.query(Model).filter(Model.name==model_id).one().client_id

  def objects(self, protocol=None, purposes=None, model_ids=None, groups=None,
      classes=None, finger_ids=None, session_ids=None):
    """Returns a set of Files for the specific query by the user.

    Keyword Parameters:

    protocol
      One of the UTFVP protocols ('master', 'paper').

    purposes
      The purposes required to be retrieved ('enrol', 'probe', 'train') or a tuple
      with several of them. If 'None' is given (this is the default), it is
      considered the same as a tuple with all possible values. This field is
      ignored for the data from the "world" group.

    model_ids
      Only retrieves the files for the provided list of model ids.
      If 'None' is given (this is the default), no filter over
      the model_ids is performed.

    groups
      One of the groups ('dev', 'world') or a tuple with several of them.
      If 'None' is given (this is the default), it is considered the same as a
      tuple with all possible values.

    classes
      The classes (types of accesses) to be retrieved ('client', 'impostor')
      or a tuple with several of them. If 'None' is given (this is the
      default), it is considered the same as a tuple with all possible values.

    finger_ids
      Only retrieves the files for the provided list of finger ids.
      If 'None' is given (this is the default), no filter over
      the finger_ids is performed.

    session_ids
      Only retrieves the files for the provided list of session ids.
      If 'None' is given (this is the default), no filter over
      the session_ids is performed.

    Returns: A list of files which have the given properties.
    """

    protocols = self.check_parameters_for_validity(protocol, "protocol", self.protocol_names())
    purposes = self.check_parameters_for_validity(purposes, "purpose", self.purposes())
    groups = self.check_parameters_for_validity(groups, "group", self.groups())
    classes = self.check_parameters_for_validity(classes, "class", ('client', 'impostor'))

    from six import string_types
    if model_ids is None:
      model_ids = ()
    elif isinstance(model_ids, string_types):
      model_ids = (model_ids,)
    import collections
    if finger_ids is None:
      finger_ids = ()
    elif not isinstance(finger_ids, collections.Iterable):
      finger_ids = (finger_ids,)
    if session_ids is None:
      session_ids = ()
    elif not isinstance(session_ids, collections.Iterable):
      session_ids = (session_ids,)

    # Now query the database
    retval = []
    if 'world' in groups:
      q = self.query(File).join((ProtocolPurpose, File.protocolPurposes)).join(Protocol).\
            filter(and_(Protocol.name.in_(protocols), ProtocolPurpose.sgroup == 'world'))
      #filter(File.sgroup == 'world')
      if finger_ids:  q = q.filter(File.finger_id.in_(finger_ids))
      if session_ids: q = q.filter(File.session_id.in_(session_ids))
      q = q.order_by(File.client_id, File.finger_id, File.session_id)
      retval += list(q)

    if 'dev' in groups:
      if 'enrol' in purposes:
        q = self.query(File).join(Client).join((ProtocolPurpose, File.protocolPurposes)).join(Protocol).\
              filter(and_(Protocol.name.in_(protocols), ProtocolPurpose.sgroup == 'dev', ProtocolPurpose.purpose == 'enrol'))
        if model_ids:   q = q.join((Model, File.models)).filter(Model.name.in_(model_ids))
        if finger_ids:  q = q.filter(File.finger_id.in_(finger_ids))
        if session_ids: q = q.filter(File.session_id.in_(session_ids))
        q = q.order_by(File.client_id, File.finger_id, File.session_id)
        retval += list(q)
        
      if 'probe' in purposes:
        if 'client' in classes:
          q = self.query(File).join(Client).join((ProtocolPurpose, File.protocolPurposes)).join(Protocol).\
                filter(and_(Protocol.name.in_(protocols), ProtocolPurpose.sgroup == 'dev', ProtocolPurpose.purpose == 'probe'))
          if len(model_ids) != 0: # Optimization using prior knowledge on the protocol to avoid long query in this case
            q = q.join((Model, Protocol.models)).filter(and_(File.client_id == Model.client_id, File.id != Model.file_id))
          if model_ids:   q = q.filter(Model.name.in_(model_ids))
          if finger_ids:  q = q.filter(File.finger_id.in_(finger_ids))
          if session_ids: q = q.filter(File.session_id.in_(session_ids))
          q = q.order_by(File.client_id, File.finger_id, File.session_id)
          retval += list(q)
       
        if 'impostor' in classes:
          q = self.query(File).join(Client).join((ProtocolPurpose, File.protocolPurposes)).join(Protocol).\
                filter(and_(Protocol.name.in_(protocols), ProtocolPurpose.sgroup == 'dev', ProtocolPurpose.purpose == 'probe'))
          if len(model_ids) != 0: # Optimization using prior knowledge on the protocol to avoid long query in this case
            q = q.join((Model, Protocol.models)).filter(File.client_id != Model.client_id)
          if model_ids:   q = q.filter(Model.name.in_(model_ids))
          if finger_ids:  q = q.filter(File.finger_id.in_(finger_ids))
          if session_ids: q = q.filter(File.session_id.in_(session_ids))
          q = q.order_by(File.client_id, File.finger_id, File.session_id)
          retval += list(q)

    return list(set(retval)) # To remove duplicates

  def protocol_names(self):
    """Returns all registered protocol names"""

    l = self.protocols()
    retval = [str(k.name) for k in l]
    return retval

  def protocols(self):
    """Returns all registered protocols"""

    return list(self.query(Protocol))

  def has_protocol(self, name):
    """Tells if a certain protocol is available"""

    return self.query(Protocol).filter(Protocol.name==name).count() != 0

  def protocol(self, name):
    """Returns the protocol object in the database given a certain name. Raises
    an error if that does not exist."""

    return self.query(Protocol).filter(Protocol.name==name).one()

  def purposes(self):
    return ProtocolPurpose.purpose_choices
