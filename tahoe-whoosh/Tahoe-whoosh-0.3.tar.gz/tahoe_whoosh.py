#!/usr/bin/env python

import logging
import threading
import re
from io import BytesIO

import requests

from whoosh.util import random_name
from whoosh.filedb.filestore import Storage
from whoosh.filedb.structfile import StructFile

# Exceptions
class StorageError(Exception):
    pass

class ReadOnlyError(StorageError):
    pass

class IncorrectCAPException(StorageError):
    """
    This exception is raised when the CAP provided isn't of the correct format.
    """
    def __init__(self, cap, expected):
        self.cap = re.split('([A-Z]+):', cap)
        self.expected = expected

    def __repr__(self):
        print("Expecting %s got a %s cap", self.expected, self.cap)

# Locking mechanism
class TahoeLock(object):
    """
    This class will be used as a locking mechanism using a CAP stored in Tahoe
    """
    def __init__(self, cap):
        """
        We need a cap (well, a full URL to a cap) to initialize.
        """
        self.cap = cap
        self.locked = False

    def acquire(self, blocking=True):
        """
        We need to check if the cap is available. If it does not exists, we then need to create it.
        If it exists we just have to wait.
        """
        # If we're in a blocking state
        if blocking:
            while True:
                try:
                    # Loop on trying to get head status on the self.cap
                    r = requests.head(self.cap)
                    r.raise_for_status()
                except:
                    # If we have an exception, it means it does not exists, so no Locks
                    # We just create it, with an empty file
                    r = requests.put(self.cap, data=None)
                    # And break out of loop
                    break
                # Else we loop
                continue
            self.locked = True
            return self.locked

        # We're in non blocking state
        else:
            try:
                # Let's check if the file exist
                r = requests.head(self.cap)
                r.raise_for_status()
            except:
                # The file does not exist
                r = requests.put(self.cap, data=None)
                # Wo we lock
                self.locked = True
                return self.locked
            else:
                # We are already locked, so exit
                return False

    def release(self):
        """
        We just need to free - delete - the cap.
        """
        try:
            r = requests.delete(self.cap)
            r.raise_for_status()
        except Exception as e:
            # We weren't able to delete teh lock … sometning went wild
            raise threading.ThreadError
        self.locked = False
        return

class TahoeStorage(Storage):
    """
    This is a class to build a whoosh index into Tahoe LAFS filesystem, using the Tahoe WebAPI
    """
    def __init__(self, base_url="http://127.0.0.1:3456/uri", base_cap="", readonly=False, debug=False):
        """We need some specific variables in order for tahoe to work:
        base_url is where the tahoe web interface is listening at, defaults to
            http://127.0.0.1:3456/uri
        base_cap is the base capability used to get the root of whoosh index, defaults
            to an empty strng.
        """
        self.base_url=base_url
        self.base_cap=base_cap
        self.locks = {}
        self.readonly = readonly

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, '/'.join([self.base_url, self.base_cap]))

    def close(self):
        """
        Close the index, since we're using only URL, nothing to do here.
        """
        pass

    def create(self):
        """
        Let's create a new index, we need to POST to base_url/base_cap if base_cap is not null.
        """
        if self.readonly:
            raise ReadOnlyError

        if self.base_cap == "":
            url = self.base_url
        else:
            url = '/'.join([self.base_url, self.base_cap])

        try:
            r = requests.post(url, params={'t': 'mkdir', 'format': 'mdmf'})
            r.raise_for_status()
        except Exception as e:
            logging.error("No response from the TAHOE-Grid. Error was: %s", e)

        if self.base_cap == "":
            self.base_cap = r.content.decode('utf8')

        return self

    def destroy(self):
        """
        Removes any files in this storage object. Leaving only an empty dir
        that won't be accessed so won't take any space. Can't remove it for now.
        """
        if self.readonly:
            raise ReadOnlyError

        url = "/".join([self.base_url, self.base_cap])

        #clean the DIRCAP
        self.clean()

    def create_file(self, name, mode="wb", **kwargs):
        """
        Creates a file with the given name in this storage.
        return a TahoeStructFile instance
        """
        if self.readonly:
            raise ReadOnlyError

        url = '/'.join([self.base_url, self.base_cap, name])
        try:
            r = requests.put(url, params={'format': 'chk'})
            r.raise_for_status()
        except Exception as e:
            logging.error("Unable to create file %s - %s" % (url, e))

        # The file is created so far so good. Need to return a fileobj
        return TahoeStructFile(url, name=name)

    def open_file(self, name, **kwargs):
        """
        Let's open a file by its name. Return a TahoeStructFile
        """
        # First let's check if it exists
        if self.file_exists(name):
            return TahoeStructFile(url, name=name)
        raise StorageError("File %s does not exist" % (name,))

    def list(self):
        """
        List all the files in teh current storage.
        """
        url = '/'.join([self.base_url, self.base_cap])
        try:
            r = requests.get(url, params={'t': 'json'})
            r.raise_for_status()
        except Exception as e:
            logging.error("Directory does not exist %s - %s" % (url, e))
            raise

        # The first item on the list is the type of node, so need to get the 
        # second one.
        if r.json()[0] != u'dirnode':
            return []
        return r.json()[1]['children'].keys()

    def clean(self, ignore=False):
        """
        Function used to empty a directory. We will walk recursively through a Storage instance
        using TahoeStorage.list() method and delet all files in it. if ignore is set to True, we
        will raise exceptions.
        """
        if self.readonly:
            raise ReadOnlyError

        # Let's just delete each file inside a directory
        for child in self.list():
            try:
                self.delete_file(child)
            except Exception as e:
                if not ignore:
                    raise

    def file_exists(self, name):
        """
        We have to test if a file exist. Just send a requests to the base_url + base_cap + name to check that.
        We just need to check the existence of file, not to get it's content, so go for a requests.head() call
        """
        url = '/'.join([self.base_url, self.base_cap, name])
        try:
            r = requests.head(url)
            r.raise_for_status()
        except:
            return False
        return True

    def _getmetadata(self, name):
        """
        Private method to get all metadata associated to a file. In tahoe, it's only needed to to a simple get
        on a file, with the t=json params.
        We return an array from the json.
        """
        url = '/'.join([self.base_url, self.base_cap, name])
        try:
            r = requests.get(url, params={'t': 'json'})
            r.raise_for_status()
        except Exception as e:
            logging.error("No such file %s - %s" % (url, e))

        logging.debug("Metadata: %s" % (r.json()[1],))
        return r.json()[1]

    def file_modified(self, name):
        """
        Let's find when a file has been modified on the tahoe instance. We need metadata for that.
        Depending on the type fo file, it can be stocked n two different places metadata[mtime] or
        metadata[tahoe][linkmotime].
        """
        metadata = self._getmetadata(name)['metadata']

        if u'mtim' in metadata.keys():
            return metadata['mtime']

        return metadata['tahoe']['linkmotime']

    def file_length(self, name):
        """
        Let's get tje file_length of base_uri + base_cap + name. It's right under _getmetadata['size']
        """
        return self._getmetadata(name)['size']

    def delete_file(self, name):
        """
        Deleting a file from tahoe - given it's RESTfull API - is as easy as a DEL /base_cap/name.
        requests.delete is good for us.
        """
        if self.readonly:
            raise ReadOnlyError

        url = '/'.join([self.base_url, self.base_cap, name])
        try:
            r = requests.delete(url)
            r.raise_for_status()
        except Exception as e:
            logging.error("Can't delete file %s - %s" % (url, e))
            raise StorageError

    def rename_file(self, oldname, newname, safe=False):
        """
        Let's use the POST call to rename a child of a directory
        """
        if self.readonly:
            raise ReadOnlyError

        url = '/'.join([self.base_url, self.base_cap])
        try:
            r = requests.post(url, params={'t': 'rename', 'from_name': 'oldname', 'to_name': 'newname'})
            r.raise_for_status()
        except Exception as e:
            logging.error("Can't relink file %s to %s - %s" % (oldname, newname, e))

    def lock(self, name):
        """
        Since files aren't locally stored (Except BytesIO for open files)
        We use the TahoeLock() mechanism to keep a track of locke files.
        """
        url = '/'.join([self.base_url, self.base_cap, name])
        if name not in self.locks:
            self.locks[name] = TahoeLock(url)
        return self.locks[name]

    def temp_storage(self, name=None):
        """
        Creates a temporary storage stored in a TahoeStorage
        We will create it as a subpart of our current location. For that we will need to
        create a new directory
        It returns a TahoeStorage instance
        """
        name = name or "%s.tmp" % random_name()
        url = '/'.join([self.base_url, self.base_cap, name])
        try:
            r = requests.put(url, params={'format': 'chk', 't': 'mkdir'})
            r.raise_for_status()
        except Exception as e:
            logger.error("Can't create temp_storage %s - %s" % (url, e))
        tempstore = TahoeStorage(base_url=self.base_url, base_cap=r.content.decode('utf8'))
        return tempstore.create()

class TahoeStructFile(StructFile):
    """
    This class is a subclass of whoosh.StructFile.
    """
    def _get(self):
        """
        This private method is used to get the file and issue the request. It returns a stream
        to be used as a classic file.
        """
        try:
            r = requests.get(self.url, stream=True)
            r.raise_for_status()
        except Exception as e:
            logging.error("Cannot read %s - %s" % (self.url, e))

        return r

    def __init__(self, url, name=None, onclose=None):
        """
        Initialise the TahoeStructFile. url is where the file is, name is the filename
        and onclose are things that need to be done when everything is closed.
        file is a BytesIO, used to store the content of the file.
        """
        self.url = url
        self._name = name
        self.onclose = onclose
        self.is_closed = False

        # Loading the file when initialising
        logging.debug("Loading file %s:%s" % (self._name, self.url))
        self.file = BytesIO(self._get().raw.read())

        # We're not on a real filesystem
        self.is_real = False

    def read(self, *args, **kwargs):
        """
        Let's read the file.
        """
        logging.debug("Reading file %s:%s of size %s" % (self._name, self.url, self.file.__sizeof__()))
        return self.file.read(*args, **kwargs)

    def close(self):
        """
        Close the locally cached file and write any change to the tahoe grid.
        """
        # First, let's get back to the start of the file
        self.file.seek(0)
        try:
            r = requests.put(self.url, data=self.file.read())
            r.raise_for_status()
        except Exception as e:
            logging.error("Cannot close file %s - %s" % (self.url, e))
            raise

        logging.debug("Closing file %s at URL %s" % (self._name, self.url))
        self.file.close()
        self.is_closed = True
