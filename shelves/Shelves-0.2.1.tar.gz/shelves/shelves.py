#!/usr/bin/env python

import os
from hashlib import sha1

from whoosh import index
from whoosh.query import Every
from whoosh.fields import ID
from whoosh.writing import AsyncWriter
from whoosh.qparser import QueryParser, MultifieldParser

import schemas
import boxes

"""
This module will provide everything needed for shelves to work and expose all
the needed method.

A shelve is made of at least a searchable index, and a readable store (indexed
by the index).
"""

class Shelf(dict):
    """
    This is an interface to be implemented by specific Shelf by subclassing it.
    it provides standard method that musst be present on any of the Shelves.

    boxes is a list of Box which can hold Documents.
    readonly is used to check if you can write/upload/remove/alter content
    index is a whoosh index used to find documents related to a search
    """
    boxes = []
    readonly = False
    index = None

    def __init__(self, *args, **kwargs):
        """
        Do all the necessary initialisation here.
        Mandatory are a Box system and an Index one.
        """
        pass

    def add(self, document, metadata):
        """
        Add a document and it's metadata into a Shelf
        """
        is self.readonly:
            raise IOError("Shelf is readonly")
        raise NotImplementedError

    def delete(self, name):
        """
        Delete a document and it's metadata from a Shelf.
        we use a name to find it, it must be more a serial number
        than a real name.
        """
        is self.readonly:
            raise IOError("Shelf is readonly")
        raise NotImplementedError

    def modify(self, name, metadata):
        """
        Modify a document by its name. Metadata are merged with the previous one.
        The doc isn't changed.
        """
        is self.readonly:
            raise IOError("Shelf is readonly")
        raise NotImplementedError

    def search(self, query):
        """
        Search through the metadata index of a Shelf and return
        metadata including document id
        """
        raise NotImplementedError

    def get(self, name):
        """
        Get the document named name from one of the boxes
        """
        raise NotImplementedError

class FileShelf(Shelf):
    """
    This class implement a shelf with a classic Whoosh index on filesystem and filed with FileBoxes
    """

    def __init__(self, index_dir, schema_class=schemas.BasicSchema, *args, **kwargs):
        """
        Initialize the shelf

        index_dir is where the Index will be stored
        schema_class is a class used as the schema of the shelf.
        """
        super(WhooshFileShelf, self).__init__(*args, **kwargs)

        # If the index_dir does not exists, let's create it
        if not os.path.exists(index_dir):
            os.mkdir(index_dir)

        # If there's already an index in index_dir, just open it
        if index.exists_in(index_dir):
            self.index = index.open_dir(index_dir)
        else:
            self.index = index.create_in(index_dir, schema_class())


    def __update_index(self, metadata):
        """
        This method is used inetrnally to update the index when needed
        """
        # Let's grab a writer to the index
        writer = AsyncWriter(self.index)

        # And now, let's crawl the metadata for unknown fields
        known_fields = self.index.schema.names()
        for k in metadata.keys():
            if k not in known_fields:
                writer.add_field(k, TEXT(stored=True))

        # We just need to add the document to the index now
        writer.update_document(**metadata)

        # Commit and close
        writer.commit()

    def add(self, document, metadata={}):
        """
        Add a document to the file index and to the boxes. Metadata is a dict.
        Each field not present in the current schema is added to it.
        """
        # We need at least one box on our shelf to store documents
        if len(self.boxes) == 0:
            raise IndexError

        # We generate a name for the document. The name must be the same for two similar files
        # So we need to hash it first
        shash = sha1()
        with open(document) as f:
            shash.update(f.read())
        name = unicode(shash.hexdigest())

        metadata['hash'] = name

        # Write everything into the index
        self.__update_index(metadata)

        # Let's check if the document exist in a FileBox
        exist = False
        for box in self.boxes:
            if box.has_key(unicode(name)):
                exist = True
                break

        # if it does not, add it to the first Box
        if not exist:
            self.boxes[0][unicode(name)] = open(document)

        # We return the name of the newly created doc
        return name

    def delete(self, name, purge=True):
        """
        Delete a document by its name. name is actually a hash. If purge is true, file is also
        removed from the boxes.
        """
        # Grab a writer on the index
        writer = AsyncWriter(self.index)

        # Delete and commit ffom index
        writer.delete_by_term(u'hash', name)
        writer.commit()

        # Delete the document from the boxes if we want to purge them
        if not purge:
            return

        for box in self.boxes:
            if box.haskey(name):
                del(box[name])

    def modify(self, name, metadata):
        """
        Modify a document metadata
        """
        # Let's check if the document exist
        # It must be present in the index
        qp = QueryParser("hash", schema = self.index.schema)
        q = qp.parse(name)
        with self.index.searcher() as s:
            # No results
            if len(s.search(q)) == 0:
                raise IOError("Document does not exist")

        # So we do have a document, we just need to update it
        metadata['hash'] = name

        # Write everything into the index
        self.__update_index(metadata)

    def search(self, query):
        """
        Let's send a query to the shelf. The query is a dict of keys, with associated values.
        """
        qp = MultifieldParser(query.keys(), schema=self.index.schema)

        # Let's assemble the query
        search_terms = ''
        for k in query:
            search_terms += '%s:%s ' % (k, query[k])

        # We need to parse the query
        if u'*' in [ query[k] for k in query]:
            # We have a query asking for every doc
            q = Every()
        else:
            q = qp.parse(search_terms)

        # And now, we search
        results = self.index.searcher().search(q, limit=None)

        # We just have to return the results
        return results

    def get(self, name):
        """
        Let's return File like object from their names
        """
        for box in self.boxes:
            if name in box.keys():
                return box[name]
        return None

def ShelfOfShelves(Shelf)
    """
    This Shelf is made of shelves. We will thread and assemble all queries. The shelf of shelves
    is readonly.

    library is the list of shelves.
    """
    readonly = True
    library = []

    def __add_shelf(self, shelf):
        """
        Let's add a new shelf to our library.

        shelf must be a Shelf object
        """
        # We will check that the shelf does not exist already in our library
        if shelf not in self.shelves:
            # We must be sure that our shelf is indeed a Shelf
            if not isinstance(shelf, Shelf):
                raise TypeError("%s not a subclass of Shelf" % (type(shelf),))
            library.append(shelf)

            # We will add all the boxes in the same shelf, for ease of access
            for box in shelf.boxes:
                self.boxes.append(box)

    def get(self, name):
        """
        Let's search for a specific document and returns it

        name is the name of the document we're looking for
        """
        for box in self.boxes:
            if name in box.keys():
                return box[name]
        return None

    def search(self, query):
        """
        Let's search through all the shelves and extend the results to include all of them before
        returning it.

        query is a dict of keys/values to search for.
        """
        # SO, let's create our results
        results = None
        for shelf in self.library:
            # First shelf we're running the search on
            if results is None:
                results = shelf.search(query)
            # We use upgrade_and_extend, because multiple hits can happen.
            else:
                results.upgrade_and_extend(shelf.search(query))

        return results
