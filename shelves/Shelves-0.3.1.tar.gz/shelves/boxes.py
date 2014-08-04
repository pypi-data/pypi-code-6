#!/usr/bin/env python

import os
import errno
import sqlite3
import json
import time

import requests

"""
This module provide anything needed to create and subclass Box instancs, which
are used to store raw documents (without their metadata.
"""
class NoteEnoughPrivileges(Exception):
    pass

class Box(dict):
    """
    This is an interface to be subclassed by specific Box. It provides standard 
    method that must be present on any of its subclasses and works as a dict.

    It can be used to specialise box. Either using local filesystem, ftp, 
    distributed ones or databases one.

    Subclass of Box must implements _put, _get, _list and _del methods
    """
    def __init__(self, *args, **kwargs):
        """
        Do whatever is needed to have the box Working, like connecting to 
        databases, getting needed parameters, etc
        """
        self.update(*args, **kwargs)

    def __repr__(self, *args, **kwargs):
        """
        Let's display our Box content
        """
        result ='{'
        for (k, v) in self.items(*args, **kwargs):
            result += repr(k) + ": " + repr(v) + ","

        result = result[:-1] + '}'
        return result

    def __len__(self, *args, **kwargs):
        """
        Return the length of the box, ie the number of keys
        """
        return len(self._list(*args, **kwargs))

    def __getitem__(self, key, *args, **kwargs):
        """
        Return the File like object associated to a key
        """
        # And if it exist
        if not self.has_key(key, *args, **kwargs):
            raise IndexError

        return self._get(key, *args, **kwargs)

    def __setitem__(self, key, document, *args, **kwargs):
        """
        Let's assign the document to a specific place in the Box
        """
        self._put(key, document, *args, **kwargs)

    def __delitem__(self, key, *args, **kwargs):
        """
        Delete an item from the box
        """
        self._del(key, *args, **kwargs)

    def __iter__(self, *args, **kwargs):
        """
        Let's iterate over keys
        """
        for key in self.keys(*args, **kwargs):
            yield key

    def __contains__(self, key, *args, **kwargs):
        """
        Do we have a key in our Box
        """
        if key in self._list(*args, **kwargs):
            return True
        return False

    def iterkeys(self, *args, **kwargs):
        """
        Let's iterate over keys
        """
        self.__iter__(*args, **kwargs)

    def itervalues(self, *args, **kwargs):
        """
        Let's iterate over values
        """
        for key in self.iterkeys():
            yield self._get(key, *args, **kwargs)

    def keys(self, *args, **kwargs):
        """
        Returns the ordered file list contained in the box, which are the keys.
        """
        return self._list(*args, **kwargs)

    def values(self, *args, **kwargs):
        """
        Returns the ordered file content in the box, values are File like object.
        """
        return [ self._get(doc, *args, **kwargs) for doc in self.keys(*args, **kwargs) ]

    def items(self, *args, **kwargs):
        """
        Return the tuples (key, value) of the document in the Box
        """
        return [ (key, self._get(key, *args, **kwargs),) for key in self.keys(*args, **kwargs) ]

    def has_key(self, name, *args, **kwargs):
        """
        Check if a document with name exist in the box. Name must be a UUID.
        """
        if not name in self._list(*args, **kwargs):
            return False
        return True

    # Below are the method that needs to be subclassed by specific box systems
    def _list(self):
        """
        Returns the list of all items in the box.
        """
        raise NotImplementedError

    def _get(self, name):
        """
        Get a document from the box, should return a File like object
        """
        raise NotImplementedError

    def _put(self, name, document):
        """
        Put a document in a box. document are, generally, File like objects.

        If a document with this name exist, it will be overwritten.
        """
        raise NotImplementedError

    def _del(self, name):
        """
        Remove a document from the box.
        """
        raise NotImplementedError

class FileBox(Box):
    """
    This box use the filesystem to store document. They're all stored in a 
    directory passed as an arg to __init__
    """
    path = None
    readonly = False

    def __init__(self, path):
        """
        We will test if the path exist, and if not creates it.
        """
        super(FileBox, self).__init__()

        self.path = os.path.abspath(path)
        # We do not have a directory
        try:
            os.mkdir(self.path)
        except IOError as e:
            raise e
        except OSError as e:
            error = errno.errorcode[e.errno]
            if error == 'EEXIST':
                # The file or directory already exist
                if os.path.isfile(self.path):
                    # And it's a file
                    raise e
            else:
                # Something else happened
                raise e

    def _list(self):
        """
        Return a list of files UUID in the FileBox
        """
        return [ unicode(item) for item in os.listdir(self.path)]

    def _put(self, name, document):
        """
        Put a document in the FileBox. name must be an a hash and document
        a File-like object
        """
        # Let's go back to the origi of file
        document.seek(0)

        # Let's open the destination, it will be created if needed
        # And let's write the origin in it by block of 4096bytes
        with open(os.path.join(self.path, unicode(name)), 'wb') as destination, document as origin:
            destination.write(origin.read())

    def _get(self, name):
        """
        Let's retrieve a file from the FileBox. name must be a hash and 
        we will return a File object
        """
        try:
            return open(os.path.join(self.path, unicode(name)), 'rb')
        except:
            raise IOError

    def _del(self, name):
        """
        Let's delete a file by its name
        """
        os.remove(os.path.join(self.path, unicode(name)))

class RemoteBox(Box):
    """
    This box is, in fact, a remote shelf. We play with it by using REST API. But
    since it's a remote one we won't write in it. And so it's a readonly Box.
    """
    readonly = True
    def __init__(self, api_root=""):
        """
        We need a token_id to auth against the remote shelf. And then, to
        auth ourselves, that's somewhere we can save some time.
        """
        super(Box, self).__init__()

        self.api_root = api_root

    def _list(self):
        """
        List does not need auth, which is nice. We need to send a magic query with '*' in it.
        It will returns metadata, we just need to parse to get the media url.

        We must return a list of path.
        """
        # We will query for hash - it's a mandatory field, we sure it exist
        # and we're using the joker '*' because it will give us all the doc
        # stored there.
        data=json.dumps({'hash': '*'})
        headers={'Content-type': 'application/json'}

        results = []

        # Let's create the search.
        r = requests.put(self.api_root+'/search/', data=data, headers=headers)

        try:
            r.raise_for_status()
        except:
            return results

        # The search is in progress, we have to wait for it to be complete
        while r.json()['state'] != "done":
            r = requests.get(self.api_root+r.json()['uri']+'/')
            try:
                r.raise_for_status()
            except:
                return results

        # So now, we have an ended search query, with all the doc in them.
        for hit in r.json()['results']:
            # Each hit is a dict and have a 'doc_url' field, that's what we
            # to query at a later time.
            results.append(hit['doc_url'].split('/')[1])

        return results

    def _put(self):
        """
        We're not going to store a document in a remote-shelf, because we don't have
        the associated metadata.
        """
        raise IOError("Cannot put documents onto a remote shelf")

    def _get(self, name):
        """
        Let's get a doc by its name, the name is a hash, we just need to assemble a URL
        """
        # We do have a document, we need to get the media url. ALso, streaming for the
        # win.
        r = requests.get('/'.join([self.api_root, 'media', name, ''], stream=True)

        # If we have an exception, it means document does not exist or
        # is unavailable
        try:
            r.raise_for_status()
        except:
            raise IOError("No such document in remote shelf")

        # requests .raw attrbute supports file like method (read, etc)
        return r.raw

    def _del(self):
        """
        We're not going to delete document from a remote shelf, it might be used elsewhere.
        """
        raise IOError("Cannot delete document from a remote shelf")
