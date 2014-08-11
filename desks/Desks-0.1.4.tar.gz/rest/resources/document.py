#!/usr/bine/env python

import json
import tempfile
import os
from hashlib import sha1

import magic
from flask import current_app, request, send_file, url_for
from flask.ext import restful
from flask.ext.restful import fields, abort
from shelves import shelves, boxes

from ..common.utils import get_shelf
from ..common.auth import authenticate

docs_fields = {
    'doc_id': fields.String,
    'uri': fields.Url('doc_ep'),
    'media_url': fields.Url('media_ep'),
    'metadata': fields.Raw,
}

class DocResource(restful.Resource):
    """
    This Resource is used to manage the document. Adding them, deleting them
    and the like.
    """
    @restful.marshal_with(docs_fields)
    def get(self, doc_id):
        """
        Let's get a specific document from the shelf. We will return the metadata,
        and a link to a /media/ resources, to download the document.
        """
        # Get the shelf first.
        shelf = get_shelf()

        # We want to search for a document, so let's search by hash.
        result = shelf.search(query={'hash': unicode(doc_id)})
        # We must have a len >= 1 or we have no such document
        if result.has_exact_length():
            length = len(result)
        else:
            length = result.estimated_length()

        if length == 0:
            abort(404, message="No document by this ID found: %s" % (doc_id,))
        # so, let's parse the result and try to find our exact match
        doc = {}
        for hit in result:
            if hit['hash'] == unicode(doc_id):
                # Yay!
                doc['metadata'] = {}
                doc['doc_id'] = hit['hash']
                for key in hit:
                    doc['metadata'][key] = hit[key]
                return doc

        # No exact match, ABORT
        abort(404, message="No document by this ID found: %s" % (doc_id,))

    @authenticate
    @restful.marshal_with(docs_fields)
    def put(self, doc_id=""):
        """
        We're going to create a new document. If it existed before, we're
        going to delete it first then create it.
        """
        # Get the shelf
        shelf = get_shelf()

        # Temp storage needed
        tempfile.tempdir = os.path.abspath(current_app.config['TEMP_UPLOAD_DIR'])

        # We need to have a metdata field
        if 'metadata' not in request.values.keys():
           abort(400, message="We need to have a metadata item in our request.")

        # We need to have one, and only one, file
        if len(request.files) != 1:
            abort(406, message="We must have one and only one file in our request. We had %s. This is unacceptable" % len(request.files))

        # The name of file is a hash, so we must check that we indeed received 
        # all the file.
        # Let's search for the document
        doc = shelf.get(doc_id)
        if doc is not None:
            # We do have a document so, let's remove it and recreates it.
            shelf.delete(doc_id)

        # We need to save the file at a temp place
        tf = tempfile.NamedTemporaryFile(delete=False)
        tf.close()

        # Save the request file in place of the tempfile
        request.files['file'].save(tf.name)
        # Let's hash the file
        shash = sha1()

        with open(tf.name) as upload:
            shash.update(upload.read())

        # So the file we're uploading does not match the doc_id, and the doc_id has been given
        if shash.hexdigest() != doc_id and doc_id != "":
            abort(400, message="Wrong file uploaded or wrong doc_id, hash mismatch")

        # Everything is ok, create the doc!!
        shelf.add(tf.name, json.loads(request.values['metadata']))

        # And let's delete the temporary file
        os.remove(tf.name)

        return {'doc_id': shash.hexdigest(), 'metadata': request.values['metadata']}

    @authenticate
    @restful.marshal_with(docs_fields)
    def post(self, doc_id=""):
        """
        We're going to update metadata about a document.
        """
        # Get the shelf
        shelf = get_shelf()

        # We need to have a metadata field
        if 'metadata' not in request.values.keys():
            abort(400, message="We need to have metadata in our request.")

        # The doc_id must be a valid existing document.
        exist = False
        for box in shelf.boxes:
            if doc_id in box.keys():
                exist = True
                break

        if not exist:
            abort(404, message="Document id %s not found" % (doc_id,))

        # Now, let's modify the metadata
        shelf.modify(doc_id, json.loads(request.values['metadata']))

        return {'doc_id': doc_id, 'metadata': request.values['metadata']}

    @authenticate
    @restful.marshal_with(docs_fields)
    def delete(self, doc_id=""):
        """
        Let's delete a file
        """
        # Get the shelf
        shelf = get_shelf()

        # Let's delete the document
        # But only if it exist
        exist = False
        for box in shelf.boxes:
            if doc_id in box.keys():
                exist = True
                break

        if not exist:
            abort(404, message="Document id %s not found" % (doc_id,))

        # Delete!!!
        shelf.delete(doc_id)

        return {}

def mediaResource(doc_id):
    """
    This function is used to stream a media to a client.
    """
    shelf = get_shelf()

    # Let's grab the file
    doc = shelf.get(doc_id)
    if doc is None:
        abort(404, message="Media id %s not found" % (doc_id,))

    # Go back to the beginning
    doc.seek(0)
    return send_file(doc)
