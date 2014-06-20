import base64
import hashlib
import logging
import os

from .item_uploader import ItemUploader

log = logging.getLogger(__name__)


class DocumentUploader(object):
    """Document uploader class which simplifies the indexing of office
    documents. Default parameters are loaded from your home directories
    .squirrorc. See the documentation of :class:`ItemUploader` for a complete
    list of options regarding project selection, source selection,
    configuration, etc.

    :param batch_size: Number of items to send in one request.
    :param metadata_mapping: A dict which contains the meta-data mapping.
    :param default_mime_type_keyword: If set to ``True`` a default keyword
        is added to the document which contains the mime-type.

    Typical usage:

        >>> from squirro_client import DocumentUploader
        >>> uploader = DocumentUploader(project_title='My Project', token='<your token')
        >>> uploader.upload('~/Documents/test.pdf')
        >>> uploader.flush()

    Meta-data mapping usage:

    * By default (i.e. for all document mime-types) map the original document
      size to a keyword field named "Doc Size":

        >>> mapping = {'default': {'sq:size_orig': 'Doc Size', 'sq:content-mime-type': 'Mime Type'}}
        >>> uploader = DocumentUploader(metadata_mapping=mapping)

    * For a specific mime-type (i.e.
      'application/vnd.oasis.opendocument.text') map the "meta:word-count"
      meta-data filed value to a keyword field named "Word Count":

        >>> mapping = {'application/vnd.oasis.opendocument.text': {'meta:word-count': 'Word Count'}}
        >>> uploader = DocumentUploader(metadata_mapping=mapping)

    Notice that the keyword field names which are specified in the meta-data
    mapping are required to only contain the following characters:

    * Alphanumeric characters (``A-Za-z0-9``)
    * Underscore (``_``)
    * Single space
    * Minus sign (``-``)
    * Plus sign (``+``)
    * Dot (``.``)

    Default meta-data fields available for mapping usage:

    * ``sq:doc_size``: Converted document file size.
    * ``sq:doc_size_orig``: Original uploded document file size.
    * ``sq:content-mime-type``: Document mime-type specified during upload
      operation.

    """

    # simple lookup table which maps file extensions to mime-types
    EXTENSION_LOOKUP = {
        '.pdf': 'application/pdf',

        '.doc': 'application/vnd.ms-word',
        '.docx': 'application/vnd.openxmlformats-officedocument.'
                 'wordprocessingml.documentapplication/zip',

        '.odt': 'application/vnd.oasis.opendocument.text',

        '.xls': 'application/vnd.ms-excel',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.'
                 'spreadsheetml.sheet',

        '.ppt': 'application/vnd.ms-powerpoint',
        '.pptx': 'application/vnd.openxmlformats-officedocument.'
                 'presentationml.presentation',

        '.rtf': 'text/rtf',

        '.odt': 'application/vnd.oasis.opendocument.text',
        '.ods': 'application/vnd.oasis.opendocument.spreadsheet',
        '.odp': 'application/vnd.oasis.opendocument.presentation',

        '.sxw': 'application/vnd.sun.xml.writer',
    }

    def __init__(self, metadata_mapping=None, batch_size=100,
                 default_mime_type_keyword=True, **kwargs):

        if metadata_mapping is None:
            metadata_mapping = {}

        # assemble processing configuration
        proc_config = {
            'content-conversion': {
                'enabled': True,
                'metadata-mapping': {
                    'default': {}
                }
            }
        }
        mapping = proc_config['content-conversion']['metadata-mapping']
        mapping.update(metadata_mapping)

        if default_mime_type_keyword and \
                'sq:content-mime-type' not in mapping['default']:
            mapping['default']['sq:content-mime-type'] = 'MIME Type'

        # check for an explicit processing config
        if 'processing_config' in kwargs:
            proc_config.update(kwargs.get('processing_config'))
            del kwargs['processing_config']

        # item uploader
        self.batch_size = batch_size
        self.uploader = ItemUploader(
            batch_size=batch_size, processing_config=proc_config, **kwargs)

        # internal state
        self._items = []

    def upload(self, filename, mime_type=None, title=None, doc_id=None):
        """Method which will use the provided ``filename`` to create a Squirro
        item for upload. Items are buffered internally and uploaded according
        to the specified batch size. If `mime_type` is not provided a simple
        filename extension based lookup is performed.

        :param filename: Read content from the provided filename.
        :param mime_type: Optional mime-type for the provided filename.
        :param title: Optional title for the uploaded document.
        """

        # get the filename extension
        root, ext = os.path.splitext(filename)

        # do some simple mime-type lookup by the filename extension and bail
        # out if we receive something unknown
        mime_type = self.EXTENSION_LOOKUP.get(ext)
        if not mime_type:
            msg = '%s document not supported' % (ext)
            log.warn(msg)
            raise Exception(msg)

        # read the raw file content and encode it
        raw = open(filename, 'rb').read()
        content = base64.b64encode(raw)

        # build a checksum over the original file content and use it as the
        # item identifier
        item_id = doc_id or hashlib.sha256(raw).hexdigest()

        # free up the memory
        raw = None

        item = {
            'content-encoding': 'base64', 'content-mime-type': mime_type,
            'content': content, 'id': item_id,
        }

        # check if an explicit title was provided, otherwise the content
        # conversion step will figure something out
        if title is not None:
            item['title'] = title

        # upload items
        self._items.append(item)
        if len(self._items) >= self.batch_size:
            self.flush()

    def flush(self):
        """Flush the internal buffer by uploading all documents."""
        if self._items:
            self.uploader.upload(self._items)
            self._items = []
