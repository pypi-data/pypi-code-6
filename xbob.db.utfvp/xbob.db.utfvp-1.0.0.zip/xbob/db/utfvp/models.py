#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
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

"""Table models and functionality for the UTFVP database.
"""

import os, numpy
import bob.db.utils
from sqlalchemy import Table, Column, Integer, String, ForeignKey, or_, and_, not_
from bob.db.sqlalchemy_migration import Enum, relationship
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declarative_base

import xbob.db.verification.utils

Base = declarative_base()

protocolPurpose_file_association = Table('protocolPurpose_file_association', Base.metadata,
  Column('protocolPurpose_id', Integer, ForeignKey('protocolPurpose.id')),
  Column('file_id', Integer, ForeignKey('file.id')))

protocol_model_association = Table('protocol_model_association', Base.metadata,
  Column('protocol_id', Integer, ForeignKey('protocol.id')),
  Column('model_id', Integer, ForeignKey('model.id')))

class Client(Base):
  """Database clients, marked by an integer identifier and the group they belong to"""

  __tablename__ = 'client'

  # Key identifier for the client
  id = Column(String(20), primary_key=True)
  subclient_id = Column(Integer)

  def __init__(self, id, subclient_id):
    self.id = id
    self.subclient_id = subclient_id

  def __repr__(self):
    return "Client(%s)" % (self.id,) 

class Model(Base):
  """Database models, marked by an integer identifier and the group they belong to"""

  __tablename__ = 'model'

  # Key identifier for the client
  id = Column(Integer, primary_key=True)
  # Name of the protocol associated with this object
  name = Column(String(20))
  # Key identifier of the client associated with this model
  client_id = Column(String(20), ForeignKey('client.id')) # for SQL
  # Key identifier of the enrollment associated with this model
  file_id = Column(Integer, ForeignKey('file.id')) # for SQL

  # For Python: A direct link to the client object that this model belongs to
  client = relationship("Client", backref=backref("models", order_by=id))
  # For Python: A direct link to the enrollment file object that this model belongs to
  file = relationship("File", backref=backref("models", order_by=id))

  def __init__(self, name, client_id, file_id):
    self.name = name
    self.client_id = client_id
    self.file_id = file_id

  def __repr__(self):
    return "Model(%s)" % (self.name,) 

class File(Base, xbob.db.verification.utils.File):
  """Generic file container"""

  __tablename__ = 'file'

  # Key identifier for the file
  id = Column(Integer, primary_key=True)
  # Key identifier of the client associated with this file
  client_id = Column(String(20), ForeignKey('client.id')) # for SQL
  # Unique path to this file inside the database
  path = Column(String(100), unique=True)
  # Group id
  group_choices = ('world', 'dev')
  sgroup = Column(Enum(*group_choices))
  # Identifier of the claimed client associated with this file
  finger_id = Column(Integer) 
  # Identifier of the session
  session_id = Column(Integer)

  # For Python: A direct link to the client object that this file belongs to
  client = relationship("Client", backref=backref("files", order_by=id))

  def __init__(self, client_id, path, sgroup, finger_id,  session_id):
    # call base class constructor
    xbob.db.verification.utils.File.__init__(self, client_id = client_id, path = path)
    self.sgroup = sgroup
    self.finger_id = finger_id
    self.session_id = session_id

class Protocol(Base):
  """UTFVP protocols"""

  __tablename__ = 'protocol'

  # Unique identifier for this protocol object
  id = Column(Integer, primary_key=True)
  # Name of the protocol associated with this object
  name = Column(String(20), unique=True)

  # For Python: A direct link to the Model objects associated with this Protcol
  models = relationship("Model", secondary=protocol_model_association, backref=backref("protocols", order_by=id))

  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return "Protocol('%s')" % (self.name,)

class ProtocolPurpose(Base):
  """UTFVP protocol purposes"""

  __tablename__ = 'protocolPurpose'

  # Unique identifier for this protocol purpose object
  id = Column(Integer, primary_key=True)
  # Id of the protocol associated with this protocol purpose object
  protocol_id = Column(Integer, ForeignKey('protocol.id')) # for SQL
  # Group associated with this protocol purpose object
  group_choices = ('world', 'dev')
  sgroup = Column(Enum(*group_choices))
  # Purpose associated with this protocol purpose object
  purpose_choices = ('train', 'enrol', 'probe')
  purpose = Column(Enum(*purpose_choices))

  # For Python: A direct link to the Protocol object that this ProtocolPurpose belongs to
  protocol = relationship("Protocol", backref=backref("purposes", order_by=id))
  # For Python: A direct link to the File objects associated with this ProtcolPurpose
  files = relationship("File", secondary=protocolPurpose_file_association, backref=backref("protocolPurposes", order_by=id))

  def __init__(self, protocol_id, sgroup, purpose):
    self.protocol_id = protocol_id
    self.sgroup = sgroup
    self.purpose = purpose

  def __repr__(self):
    return "ProtocolPurpose('%s', '%s', '%s')" % (self.protocol.name, self.sgroup, self.purpose)

