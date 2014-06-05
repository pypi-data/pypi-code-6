# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2014 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
import os

import re
import jinja2

from sqlalchemy import Table, Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.exc import UnboundExecutionError
from sqlalchemy.orm import relationship, validates

from stalker.db.declarative import Base
from stalker.models import check_circular_dependency
from stalker.models.link import Link

from stalker import defaults

from stalker.log import logging_level
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging_level)


class Version(Link):
    """Holds information about the created versions (files) for a class:`.Task`

    A :class:`.Version` holds information about the
    created files related to a class:`.Task`. So if one
    creates a new version for a file or a sequences of file for a
    :class:`.Task` then the information is hold in the
    :class:`.Version` instance.

    :param str take_name: A short string holding the current take name. Takes
      in Stalker are used solely for grouping individual versions together.
      Versions with the same ``take_name`` (of the same Task) are numbered
      together. It can be any alphanumeric value (a-zA-Z0-9\_). The default is
      the string "Main". When skipped it will use the default value. It can not
      start with a number. It can not have white spaces.

    :param inputs: A list o :class:`.Link` instances, holding the inputs of the
      current version. It could be a texture for a Maya file or an image
      sequence for Nuke, or anything those you can think as the input for the
      current Version.

    :type inputs: list of :class:`.Link`

    :param outputs: A list of :class:`.Link` instances, holding the outputs of
      the current version. It could be the rendered image sequences out of Maya
      or Nuke, or it can be a Targa file which is the output of a Photoshop
      file (\*.psd), or anything that you can think as the output which is
      created out of this Version.

    :type outputs: list of :class:`.Link` instances

    :param task: A :class:`.Task` instance showing the owner of this Version.

    :type task: :class:`.Task`

    :param parent: A :class:`.Version` instance which is the parent of this
      Version. It is mainly used to see which Version is derived from which in
      the Version history of a :class:`.Task`.

    :type parent: :class:`.Version`
    """
    __auto_name__ = True
    __tablename__ = "Versions"
    __mapper_args__ = {"polymorphic_identity": "Version"}

    version_id = Column("id", Integer, ForeignKey("Links.id"),
                        primary_key=True)
    task_id = Column(Integer, ForeignKey("Tasks.id"), nullable=False)
    task = relationship(
        "Task",
        primaryjoin="Versions.c.task_id==Tasks.c.id",
        doc="""The :class:`.Task` instance that this Version is created for.
        """,
        uselist=False,
        back_populates="versions",
    )

    take_name = Column(
        String(256),
        default=defaults.version_take_name,
        doc="""Takes in Versions are used solely for grouping individual
        versions together."""
    )

    version_number = Column(
        Integer,
        default=1,
        nullable=False,
        doc="""The :attr:`.version_number` attribute is read-only.
        Trying to change it will produce an AttributeError.
        """
    )

    parent_id = Column('parent_id', Integer, ForeignKey('Versions.id'))
    parent = relationship(
        'Version',
        remote_side=[version_id],
        primaryjoin='Versions.c.parent_id==Versions.c.id',
        back_populates='children',
        post_update=True
    )

    children = relationship(
        'Version',
        primaryjoin='Versions.c.parent_id==Versions.c.id',
        back_populates='parent',
        post_update=True,
        doc="""The children :class:`.Version` instances which are derived from
        this particular Version instance.
        """
    )

    inputs = relationship(
        "Link",
        secondary="Version_Inputs",
        primaryjoin="Versions.c.id==Version_Inputs.c.version_id",
        secondaryjoin="Version_Inputs.c.link_id==Links.c.id",
        doc="""The inputs of the current version.

        It is a list of :class:`.Link` instances.
        """
    )

    outputs = relationship(
        "Link",
        secondary="Version_Outputs",
        primaryjoin="Versions.c.id==Version_Outputs.c.version_id",
        secondaryjoin="Version_Outputs.c.link_id==Links.c.id",
        doc="""The outputs of the current version.

        It is a list of :class:`.Link` instances.
        """
    )

    is_published = Column(Boolean, default=False)

    created_with = Column(String(256))

    def __init__(self,
                 task=None,
                 take_name=defaults.version_take_name,
                 inputs=None,
                 outputs=None,
                 parent=None,
                 full_path=None,
                 created_with=None,
                 **kwargs):
        # call supers __init__
        kwargs['full_path'] = full_path
        super(Version, self).__init__(**kwargs)

        self.take_name = take_name
        self.task = task
        self.version_number = None
        if inputs is None:
            inputs = []

        if outputs is None:
            outputs = []

        self.inputs = inputs
        self.outputs = outputs

        self.is_published = False

        self.parent = parent
        self.created_with = created_with

    def __repr__(self):
        """the representation of the Version
        """
        return "<%(project_code)s_%(nice_name)s_%(version_number)s " \
               "(%(entity_type)s)>" % \
               {
                   'project_code': self.task.project.code,
                   'nice_name': self.nice_name,
                   'version_number':
                   'v%s' % ('%s' % self.version_number).zfill(3),
                   'entity_type': self.entity_type
               }

    @classmethod
    def _format_take_name(cls, take_name):
        """formats the given take_name value
        """
        # remove unnecessary characters
        take_name = re.sub(
            r"([^a-zA-Z0-9\s_\-]+)", r"", take_name
        ).strip()

        # replace empty spaces with underscores
        take_name = re.sub(r'[\s]+', '_', take_name)

        # replace multiple underscores with only one
        # take_name = re.sub(r'([_]+)', r'_', take_name)

        # remove any non allowed characters from the start
        take_name = re.sub(r"^[^a-zA-Z0-9]+", r"", take_name)

        return take_name

    @validates("take_name")
    def _validate_take_name(self, key, take_name):
        """validates the given take_name value
        """
        if take_name is None:
            raise TypeError(
                "%s.take_name can not be None, please give a proper string" %
                self.__class__.__name__
            )

        take_name = self._format_take_name(str(take_name))

        if take_name == "":
            raise ValueError(
                "%s.take_name can not be an empty string" %
                self.__class__.__name__
            )

        return take_name

    @property
    def latest_version(self):
        """returns the Version instance with the highest version number in this
        series.

        :returns: :class:`.Version` instance
        """
        try:
            last_version = Version.query\
                .filter(Version.task == self.task)\
                .filter(Version.take_name == self.take_name)\
                .order_by(Version.version_number.desc())\
                .first()
        except UnboundExecutionError:
            last_version = None
        return last_version

    @property
    def max_version_number(self):
        """returns the maximum version number for this Version
        :return: int
        """
        latest_version = self.latest_version

        if latest_version:
            return latest_version.version_number

        return 0

    @validates("version_number")
    def _validate_version_number(self, key, version_number):
        """validates the given version_number value
        """
        # get the latest version
        # and do it with auto flush turned off,
        # or it will find itself and increase the version number unnecessarily
        from stalker.db.session import DBSession
        with DBSession.no_autoflush:
            latest_version = self.latest_version

        max_version_number = 0
        if latest_version:
            max_version_number = latest_version.version_number

        logger.debug('max_version_number: %s' % max_version_number)
        logger.debug('given version_number: %s' % version_number)

        if version_number is None or version_number <= max_version_number:
            if latest_version == self:
                version_number = latest_version.version_number
                logger.debug(
                    'the version is the latest version in database, the '
                    'number will not be changed from %s' % version_number)
            else:
                version_number = max_version_number + 1
                logger.debug(
                    'given Version.version_number is too low,'
                    'max version_number in the database is %s, setting the '
                    'current version_number to %s' % (
                        max_version_number, version_number
                    )
                )

        return version_number

    @validates("task")
    def _validate_task(self, key, task):
        """validates the given task value
        """
        if task is None:
            raise TypeError(
                "%s.task can not be None" % self.__class__.__name__
            )

        from stalker.models.task import Task

        if not isinstance(task, Task):
            raise TypeError(
                "%s.task should be a stalker.models.task.Task instance not %s"
                % (self.__class__.__name__, task.__class__.__name__)
            )

        return task

    @validates("inputs")
    def _validate_inputs(self, key, input_):
        """validates the given input value
        """
        from stalker.models.link import Link

        if not isinstance(input_, Link):
            raise TypeError(
                "All elements in %s.inputs should be all "
                "stalker.models.link.Link instances not %s" %
                (self.__class__.__name__, input_.__class__.__name__)
            )

        return input_

    @validates("outputs")
    def _validate_outputs(self, key, output):
        """validates the given output
        """
        from stalker.models.link import Link

        if not isinstance(output, Link):
            raise TypeError(
                "All elements in %s.outputs should be all "
                "stalker.models.link.Link instances not %s" %
                (self.__class__.__name__, output.__class__.__name__)
            )

        return output

    @validates('parent')
    def _validate_parent(self, key, parent):
        """validates the given parent value
        """
        if parent is not None:
            if not isinstance(parent, Version):
                raise TypeError(
                    '%s.parent should be a stalker.models.version.Version '
                    'instance, not %s' %
                    (self.__class__.__name__, parent.__class__.__name__)
                )

        # check for CircularDependency
        check_circular_dependency(self, parent, 'children')

        return parent

    @validates('children')
    def _validate_children(self, key, child):
        """validates the given child value
        """
        if not isinstance(child, Version):
            raise TypeError(
                'All elements in %s.children should be a '
                'stalker.models.version.Version instance, not %s' %
                (self.__class__.__name__, child.__class__.__name__)
            )
        return child

    def _template_variables(self):
        """variables used in rendering the filename template
        """
        from stalker import Shot

        sequences = []
        scenes = []
        if isinstance(self.task, Shot):
            sequences = self.task.sequences
            scenes = self.task.scenes

        # get the parent tasks
        task = self.task
        parent_tasks = task.parents
        parent_tasks.append(task)

        kwargs = {
            'project': self.task.project,
            'sequences': sequences,
            'scenes': scenes,
            'sequence': self.task,
            'shot': self.task,
            'asset': self.task,
            'task': self.task,
            'parent_tasks': parent_tasks,
            'version': self,
            'type': self.type,
            'extension': self.extension
        }
        return kwargs

    def update_paths(self):
        """updates the path variables
        """
        kwargs = self._template_variables()

        # get a suitable FilenameTemplate
        structure = self.task.project.structure

        from stalker import FilenameTemplate

        vers_template = None
        if structure:
            for template in structure.templates:
                assert isinstance(template, FilenameTemplate)
                if template.target_entity_type == self.task.entity_type:
                    vers_template = template
                    break

        if not vers_template:
            raise RuntimeError(
                "There are no suitable FilenameTemplate "
                "(target_entity_type == '%(entity_type)s') defined in the "
                "Structure of the related Project instance, please create a "
                "new stalker.models.template.FilenameTemplate instance with "
                "its 'target_entity_type' attribute is set to "
                "'%(entity_type)s' and assign it to the `templates` attribute "
                "of the structure of the project" % {
                    'entity_type': self.task.entity_type
                }
            )

        temp_filename = \
            jinja2.Template(vers_template.filename).render(**kwargs)

        if not isinstance(temp_filename, str):
            # it is
            # byte for python3
            # or
            # unicode for python2
            temp_filename = temp_filename.encode('utf-8')

        temp_path = \
            jinja2.Template(vers_template.path).render(**kwargs)

        if not isinstance(temp_path, str):
            # it is
            # byte for python3
            # or
            # unicode for python2
            temp_path = temp_path.encode('utf-8')

        self.filename = temp_filename
        self.path = temp_path

    @property
    def absolute_full_path(self):
        """Returns the absolute full path of this version including the
        repository path of the related project

        :return: str
        """
        project = self.task.project
        repo = project.repository

        return os.path.join(
            repo.path,
            self.full_path
        ).replace('\\', '/')

    @property
    def absolute_path(self):
        """Returns the absolute path of this version including the repository
        path of the related project

        :return: str
        """
        project = self.task.project
        repo = project.repository

        return os.path.join(
            repo.path,
            self.path
        ).replace('\\', '/')

    def is_latest_published_version(self):
        """returns True if this is the latest published Version False otherwise
        """
        if not self.is_published:
            return False

        return self == self.latest_published_version

    @property
    def latest_published_version(self):
        """Returns the last published version.

        :return: :class:`.Version`
        """
        return Version.query\
            .filter_by(task=self.task)\
            .filter_by(take_name=self.take_name)\
            .filter_by(is_published=True)\
            .order_by(Version.version_number.desc())\
            .first()

    @validates('created_with')
    def _validate_created_with(self, key, created_with):
        """validates the given created_with value
        """
        if created_with is not None:
            if not isinstance(created_with, str):
                raise TypeError(
                    '%s.created_with should be an instance of str, not %s' %
                    (self.__class__.__name__, created_with.__class__.__name__)
                )
        return created_with

    def __eq__(self, other):
        """checks equality of two version instances
        """
        return super(Version, self).__eq__(other) and \
            isinstance(other, Version) and \
            self.task == other.task and \
            self.take_name == other.take_name and \
            self.version_number == other.version_number

    def __hash__(self):
        """the overridden __hash__ method
        """
        return hash(self.id) + 2 * hash(self.name) + 3 * hash(self.entity_type)

    @property
    def naming_parents(self):
        """returns a list of parents which start from the nearest Asset, Shot
        or Sequence
        """
        # find a Asset, Shot or Sequence, and store it as the significant
        # parent, and name the task starting from that entity
        all_parents = self.task.parents
        all_parents.append(self.task)
        naming_parents = []
        if all_parents:
            significant_parent = all_parents[0]

            for parent in reversed(all_parents):
                if parent.entity_type in ['Asset', 'Shot', 'Sequence']:
                    significant_parent = parent
                    break

            # now start from that parent towards the task
            past_significant_parent = False
            naming_parents = []
            for parent in all_parents:
                if parent is significant_parent:
                    past_significant_parent = True
                if past_significant_parent:
                    naming_parents.append(parent)
        return naming_parents

    @property
    def nice_name(self):
        """the overridden nice name for Version class
        """
        naming_parents = self.naming_parents
        return self._format_nice_name(
            '_'.join(map(lambda x: x.nice_name, naming_parents)) +
            '_' + self.take_name
        )

    def walk_hierarchy(self, method=0):
        """Walks the hierarchy of this version

        :param method: The walk method, 0: Depth First, 1: Breadth First
        """
        from stalker.models import walk_hierarchy
        for v in walk_hierarchy(self, 'children', method=method):
            yield v

    def walk_inputs(self, method=0):
        """Walks the inputs of this version

        :param method: The walk method, 0: Depth First, 1: Breadth First
        """
        from stalker.models import walk_hierarchy
        for v in walk_hierarchy(self, 'inputs', method=method):
            yield v

# VERSION INPUTS
Version_Inputs = Table(
    "Version_Inputs", Base.metadata,
    Column("version_id", Integer, ForeignKey("Versions.id"), primary_key=True),
    Column("link_id", Integer, ForeignKey("Links.id"), primary_key=True)
)

# VERSION_OUTPUTS
Version_Outputs = Table(
    "Version_Outputs", Base.metadata,
    Column("version_id", Integer, ForeignKey("Versions.id"), primary_key=True),
    Column("link_id", Integer, ForeignKey("Links.id"), primary_key=True)
)
