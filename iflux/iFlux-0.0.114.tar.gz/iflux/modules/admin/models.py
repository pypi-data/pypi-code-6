# Copyright 2013-2014 Flavio Garcia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import hashlib

from sqlalchemy import CHAR, Column, SmallInteger, String
from sqlalchemy import Text, text, TIMESTAMP
from sqlalchemy.schema import Index, DefaultClause
from sqlalchemy.dialects.mysql.base import BIGINT, MEDIUMINT

import iflux.conf as iconf
from iflux.modules.admin import AdminModule
from iflux.util.sqlalchemy_util import Base

table_prefix = AdminModule.current_instance.table_prefix


class UserBase(Base):

    __tablename__ = '%s_user' % table_prefix

    mysql_engine='MyISAM'

    mysql_charset='utf8'

    # User id. This field is auto generated.
    id = Column('user_id', BIGINT(20, unsigned = True), primary_key=True)

    # User first name.
    first_name = Column('user_first_name', String(50),
                        DefaultClause(''), nullable=False)

    # User last name.
    last_name = Column('user_last_name', String(50),
                       DefaultClause(''), nullable=False)

    # User email address. This field is unique. This filed is used
    # to authenticate an user during the login process.
    email = Column('user_email', String(255),
                   DefaultClause(''), nullable=False, unique=True)

    # User password.
    password = Column('user_password', String(512),
                      DefaultClause(''), nullable=False)

    # User creation date.
    created = Column('created', TIMESTAMP,
                     DefaultClause('0000-00-00 00:00:00'), nullable=False)

    # User last update date
    updated = Column('updated', TIMESTAMP,
                     DefaultClause('0000-00-00 00:00:00'), nullable=False)


class GroupBase(Base):

    __tablename__ = 'group'

    mysql_engine='MyISAM'

    mysql_charset='utf8'

    # Group id. This field is auto generated.
    id = Column('group_id', BIGINT(20, unsigned=True), primary_key=True)

    # Group name.
    first_name = Column('group_name', String(50),
                        DefaultClause(''), nullable=False)

    # Group creation date.
    created = Column('created', TIMESTAMP,
                     DefaultClause('0000-00-00 00:00:00'), nullable=False)

    # Group last update date
    updated = Column('updated', TIMESTAMP,
                     DefaultClause('0000-00-00 00:00:00'), nullable=False)
