# -*- coding: utf-8 -*-

"""
Created on 2014-07-26
:author: Andreas Kaiser (disko)
"""

import os
from logging import getLogger
from uuid import uuid4

import transaction
from kotti.interfaces import IBlobStorage
from repoze.filesafe import create_file
from repoze.filesafe import delete_file
from repoze.filesafe import open_file
from zope.interface import implements


log = getLogger(__name__)


def create_directory(path):
    """ Check if a directory exists for the given path and create it if
    necessary.

    :param path: Absoulte path of the directory
    :type path:
    """

    if os.path.isdir(path):
        return
    else:
        os.makedirs(path, 0700)
        log.info("Directory created: %s".format(path))


def split_by_n(seq, n=2):
    """ A generator to divide a sequence into chunks of n units.

    :param seq: Sequence to be divided
    :type seq: iteratable (usually str)

    :param n: length of chunks
    :type n: int

    :result: list of chunks
    :rtype: iterable
    """

    while seq:
        yield seq[:n]
        seq = seq[n:]


class filestore(object):
    """ BLOB storage provider for Kotti that stores BLOB in the filesystem """

    implements(IBlobStorage)

    def __init__(self, url):
        """ The constructor is passed an URL containing the desired
        configuration options.

        :param config: Configuration URL
        :type config: :class:`yurl.URL`
        """

        self._path = url.path
        create_directory(self._path)

    def path(self, id='tmp'):
        """ Return the absolute path for the given file id.

        :param id: ID of the file object
        :type id: something convertable to unicode

        :result: Full path of the file
        :rtype: unicode
        """

        if id == "tmp":
            path = unicode(id)
        else:
            # Create path from id by converting to str,
            # splitting up and inserting slashes
            path = os.path.join(*split_by_n(str(id).replace("-", "")))

        #Full path is the newly created path appended to the base directory

        return os.path.join(self._path, path)

    def read(self, id):
        """ Get the data for an object with the given ID.

        :param id: ID of the file object
        :type id: unicode

        :result: Data / value of the file object
        :rtype:
        """

        f = open_file(self.path(id), mode='r')

        return f.read()

    def write(self, data):
        """ Create or update an object with the given ``id`` and write ``data``
        to its contents.

        :param data: Data / value of the file object
        :type data: ???

        :result: ID for the file object
        :rtype: str
        """

        id = uuid4()
        # TODO: call create_directory during transaction
        # check if the filepath and the tempdir exist and create if necessary
        create_directory(os.path.split(self.path(id))[0])
        create_directory(self.path())
        f = create_file(self.path(id), mode='w', tempdir=self.path())
        f.write(data)
        f.close()

        return str(id)

    def remove_base_directory(self, path):
        """ Recursively remove all empty directorys. """

        # Stop if either the base directory is reached
        # or the directory is not empty
        if path == self._path or path+"/" == self._path:
            return
        elif len(os.listdir(path)) > 0:
            return
        else:
            os.rmdir(path)
            self.remove_base_directory(os.path.split(path)[0])

    def delete(self, id):
        """ Delete the object with the given ID.

        :param id: ID of the file object
        :type id: unicode

        :result: Success
        :rtype: bool
        """

        # The kotti.events.ObjectDelete Event fires when the transaction is
        # already committing. It is safe to use os.unlink
        if transaction.get().status == "Committing":
            os.unlink(self.path(id))
            self.remove_base_directory(os.path.split(self.path(id=id))[0])
        else:
            # TODO: call remove_base_directory during transaction
            delete_file(self.path(id))
