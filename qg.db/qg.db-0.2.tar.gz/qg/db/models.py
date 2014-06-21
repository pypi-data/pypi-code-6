# -*- coding: utf-8 -*-
#
# Copyright 2013, Qunar OPSDEV
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
# Author: Jianing Yang <jianingy.yang@gmail.com>
#

from datetime import datetime
from oslo.db.sqlalchemy import models
from sqlalchemy.ext import declarative
import sqlalchemy as sa


from qg.core.timeutils import utcnow


class TableNameMixin(object):

    @declarative.declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'


class JSONSeriableMixin(object):

    def __iter__(self):
        """ Returns a JSON representation of an SQLAlchemy-backed object.
        """

        for col in self._sa_class_manager.mapper.mapped_table.columns:
            value = getattr(self, col.name)
            if isinstance(value, datetime):
                value = datetime.strftime(value, '%F %T')
            yield (col.name, value)


class HasIdMixin(object):
    id = sa.Column(sa.Integer, primary_key=True)


class TimestampMixin(object):
    created_at = sa.Column(sa.DateTime, default=utcnow)
    updated_at = sa.Column(sa.DateTime, onupdate=utcnow)

ModelBase = models.ModelBase
