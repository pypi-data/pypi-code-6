from . import item, search, catalog


# get_item()
# ________________________________________________________________________________________
def get_item(identifier, metadata_timeout=None, config=None, max_retries=1,
             archive_session=None):
    """Get an :class:`Item <Item>` object.

    :type identifier: str
    :param identifier: The globally unique Archive.org identifier for a
                       given item.

    :type metadata_timeout: int
    :param metadata_timeout: (optional) Set a timeout for retrieving an
                             item's metadata.

    :type config: dict
    :param secure: (optional) Configuration options for session.

    :type max_retries: int
    :param max_retries: (optional) Maximum number of times to request a
                        website if the connection drops.

    :returns: An :class:`Item <Item>` object.

    """
    return item.Item(identifier, metadata_timeout, config, max_retries, archive_session)


# get_files()
# ________________________________________________________________________________________
def get_files(identifier, files=None, source=None, formats=None, glob_pattern=None,
              metadata_timeout=None, config=None):
    """Get :class:`File <File>` objects, which can be filtered using
    the ``files``, ``formats``, and ``glob_pattern``, parameters. If no
    filters are provided, all :class:`File <File>` objects for the given
    item are returned.

    :type identifier: str
    :param identifier: The globally unique Archive.org identifier for a
                       given item.

    :type files: str or list
    :param files: (optional) Return :class:`File <File>` objects that
                  match any of the given filenames.

    :type source: str or list
    :param source: (optional) Return :class:`File <File>` objects that
                   are of any of the given sources.

    :type formats: str or list
    :param formats: (optional) Return :class:`File <File>` objects that
                    are of any of the given formats.

    :type glob_pattern: str
    :param glob_pattern: (optional) Return :class:`File <File>` objects
                         matching the given regular expression pattern.
                         Matching is done using :func:`fnmatch.fnmatch`.

    :type metadata_timeout: int
    :param metadata_timeout: (optional) Set a timeout for retrieving an
                             item's metadata.

    :type config: dict
    :param secure: (optional) Configuration options for session.

    :returns: a list of :class:`File <File>` objects.

    """
    item = get_item(identifier, metadata_timeout, config)
    return item.get_files(files, source, formats, glob_pattern)


# iter_files()
# ________________________________________________________________________________________
def iter_files(identifier, metadata_timeout=None, config=None):
    """A :class:`File <File>` object generator.

    :type identifier: str
    :param identifier: The globally unique Archive.org identifier for a
                       given item.

    :type metadata_timeout: int
    :param metadata_timeout: (optional) Set a timeout for retrieving an
                             item's metadata.

    :type config: dict
    :param secure: (optional) Configuration options for session.

    :returns: A generator that yields :class:`File <File>` objects.

    """
    item = get_item(identifier, metadata_timeout, config)
    return item.iter_files()


# modify_metadata()
# ________________________________________________________________________________________
def modify_metadata(identifier, metadata, target='metadata', append=False, priority=None,
                    access_key=None, secret_key=None, debug=False, metadata_timeout=None,
                    config=None):
    """Modify the metadata of an existing item on Archive.org.

    :type identifier: str
    :param identifier: The globally unique Archive.org identifier for a
                       given item.

    :type metadata: dict
    :param metadata: A dict of metadata used to modify the given item.

    :type target: str
    :param target: (optional) Set the metadata target to update.

    :type append: bool
    :param append: (optional) Append metadata to existing values.

    :type priority: int
    :param priority: (optional) Set task priority.

    :type access_key: str
    :param access_key: (optional) The IA-S3 access_key to send with the
                       request.

    :type secret_key: str
    :param secret_key: (optional) The IA-S3 secret_key to send with the
                       request.

    :type debug: bool
    :param debug: (optional) Return a :class:`requests.Request <Request>`
                  object for debugging, rather than a
                  :class:`requests.Response <Response>` object.

    :type metadata_timeout: int
    :param metadata_timeout: (optional) Set a timeout for retrieving an
                             item's metadata.

    :type config: dict
    :param secure: (optional) Configuration options for session.

    :returns: A :class:`requests.Request <Request>` object, or a
              :class:`requests.Response <Response>` object if debug
              is set to True.

    """
    item = get_item(identifier, metadata_timeout, config)
    return item.modify_metadata(metadata, target, append, priority, access_key,
                                secret_key, debug)


# upload()
# ________________________________________________________________________________________
def upload(identifier, files, metadata={}, headers={}, queue_derive=True,
           ignore_preexisting_bucket=False, verify=True, checksum=False, delete=False,
           access_key=None, secret_key=None, verbose=False, debug=False, **kwargs):
    """Upload files to an Archive.org item. The item will be created if
    it does not exist.

    :type files: str, list, dict, or list of 2-tuples.
    :param files: The filepaths or file-like objects to upload.

    :type metadata: dict
    :param metadata: (optional) Metadata used to create a new item.

    :type headers: dict
    :param headers: (optional) Add additional IA-S3 headers to request.

    :type queue_derive: bool
    :param queue_derive: (optional) Set to False to prevent an item from
                         being derived after upload.

    :type ignore_preexisting_bucket: bool
    :param ignore_preexisting_bucket: (optional) Destroy and respecify
                                      the metadata for an item

    :type verify: bool
    :param verify: (optional) Verify local MD5 checksum matches the MD5
                   checksum of the file received by IAS3.

    :type checksum: bool
    :param checksum: (optional) Skip based on checksum.

    :type delete: bool
    :param delete: (optional) Delete local file after the upload has been
                   successfully verified.

    :type access_key: str
    :param access_key: (optional) The IA-S3 access_key to send with the
                       request.

    :type secret_key: str
    :param secret_key: (optional) The IA-S3 secret_key to send with the
                       request.

    :type verbose: bool
    :param verbose: (optional) Print progress to stdout.

    :type debug: bool
    :param debug: (optional) Set to True to print headers to stdout, and
                  exit without sending the upload request.

    :param \*\*kwargs: (optional) Arguments that
                       :class:`requests.Request <Request>` takes.

    Usage::

        >>> from internetarchive import upload
        >>> md = dict(mediatype='image', creator='Jake Johnson')
        >>> upload('identifier', '/path/to/image.jpg', metadata=md, queue_derive=False)
        [<Response [200]>]

        >>> files = {'new_name.txt': 'file.txt', 'copy.txt': 'file.txt'}
        >>> upload('iacli-test-item', files, metadata=md)
        [<Response [200]>, <Response [200]>]

        >>> import StringIO
        >>> contents = 'hello world'
        >>> name = 'hello_world.txt'
        >>> fh = StringIO.StringIO(contents)
        >>> fh.name = name
        >>> upload('iacli-test-item', fh, metadata=md)
        [<Response [200]>]

    :returns: A list of :class:`requests.Response <Response>` objects,
              or a list of :class:`requests.Request <Request>` objects
              if debug is set to True.

    """
    item = get_item(identifier)
    return item.upload(files, metadata, headers, queue_derive, ignore_preexisting_bucket,
                       verify, checksum, delete, access_key, secret_key, verbose, debug,
                       **kwargs)


# download()
# ________________________________________________________________________________________
def download(identifier, filenames=None, **kwargs):
    """Download files from Archive.org

    :type filenames: str, list, set
    :param filenames: The filename(s) of the given file(s) to download.

    :type concurrent: bool
    :param concurrent: Download files concurrently if ``True``.

    :type source: str
    :param source: Only download files matching given source.

    :type formats: str
    :param formats: Only download files matching the given Formats.

    :type glob_pattern: str
    :param glob_pattern: Only download files matching the given glob
                         pattern

    :type ignore_existing: bool
    :param ignore_existing: Overwrite local files if they already
                            exist.

    :rtype: bool
    :returns: True if if files have been downloaded successfully.

    Usage::

        >>> import internetarchive
        >>> internetarchive.download('stairs', source=['metadata', 'original'])

    """
    item = get_item(identifier)
    if filenames:
        if not isinstance(filenames, (set, list)):
            filenames = [filenames]
        for fname in filenames:
            f = item.get_file(fname)
            f.download(**kwargs)
    else:
        item.download(**kwargs)


# delete()
# ________________________________________________________________________________________
def delete(identifier, filenames=None, **kwargs):
    item = get_item(identifier)
    if filenames:
        if not isinstance(filenames, (set, list)):
            filenames = [filenames]
        for f in item.iter_files():
            if f.name not in filenames:
                continue
            f.delete(**kwargs)


# get_tasks()
# ________________________________________________________________________________________
def get_tasks(**kwargs):
    _catalog = catalog.Catalog(identifier=kwargs.get('identifier'),
                               params=kwargs.get('params'),
                               task_ids=kwargs.get('task_ids'))
    task_type = kwargs.get('task_type')
    if task_type:
        return eval('_catalog.{0}_rows'.format(task_type.lower()))
    else:
        return _catalog.tasks


# search_items()
# ________________________________________________________________________________________
def search_items(query, **kwargs):
    return search.Search(query, **kwargs)


# mine()
# ________________________________________________________________________________________
def get_data_miner(identifiers, **kwargs):
    from . import mine
    return mine.Mine(identifiers, **kwargs)
