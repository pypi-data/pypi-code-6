import base64
import gzip
import logging
import mimetypes
import os
import re
import shutil
from functools import partial
from hashlib import md5
from tempfile import mkdtemp

from boto.s3.connection import OrdinaryCallingFormat, S3Connection
from flask import url_for as _url_for
from flask import request

CSS_URL_PATTERN = re.compile('url\((?:\'|")?([^\'"\)]+)(?:\'|")?\)')


class Upstatic(object):

  _compiled_paths = {}

  def __init__(self, app=None):
    if app:
      self.init_app(app)

  @property
  def use_local(self):
    return (self._app.config.get('UPSTATIC_DEBUG_USE_LOCAL', True) and
            self._app.config.get('DEBUG'))

  def _walk(self, path):
    for dirpath, _dirnames, filenames in os.walk(path):
      for filename in filenames:
        if filename.lower() not in ('.ds_store', 'thumbs.db'):
          yield os.path.join(dirpath, filename)

  def _get_md5(self, data, salt=''):
    return base64.urlsafe_b64encode(md5(salt + data).digest())

  def _is_image(self, filename):
    mimetype = mimetypes.guess_type(filename)[0]
    return mimetype and mimetype.startswith('image')

  def _is_css(self, filename):
    mimetype = mimetypes.guess_type(filename)[0]
    return mimetype and mimetype == 'text/css'

  def _key(self, *args):
    return "\0".join(map(str, args))

  def _get_compiled_path(self, path, is_gzip):
    # Get file contents
    try:
      with open(path) as f:
        data = f.read()
    except IOError:
      raise

    md5 = self._get_md5(data)
    basename = os.path.basename(path)

    # Get compiled path
    compression = 'gz' if is_gzip else 'raw'
    compiled_path = os.path.join('c', md5[:1], md5[1:7], compression, basename)

    return compiled_path

  def _css_replace_url(self, is_gzip, match):
    path = match.group(1).rsplit('#', 1)[0].rsplit('?', 1)[0]
    if path.startswith('http'):  # absolute url
      return path
    elif path.startswith('/'):  # from root
      return path
    else:  # relative to the CSS
      if self._is_image(path):
        is_gzip = False
      compiled_path = self._compiled_paths.get(
        self._key(
          path,
          is_gzip,
        ),
      )
      return "url('%s')" % self._build_url(compiled_path)

  def _fix_css(self, compiled_data, is_gzip):
    sub = partial(self._css_replace_url, is_gzip)
    return CSS_URL_PATTERN.sub(sub, compiled_data)

  def compile(self):
    self._logger.info("Compiling...")

    compiled = set()

    images = set()
    css = set()

    gzipped = set()
    raw = set()

    # Collect files
    for path in self._walk(self._app.static_folder):

      # Get relative path
      path = os.path.relpath(path)

      for is_gzip in True, False:

        # Get compiled path
        compiled_path = self._get_compiled_path(path, is_gzip)

        # Create directories
        compiled_dirname = os.path.dirname(compiled_path)
        try:
          os.makedirs(os.path.join(self._tmpdir, compiled_dirname))
        except OSError:
          pass

        # Collect images
        # NOTE: Images aren't gzipped
        if self._is_image(path):
          if is_gzip:
            continue
          else:
            images.add(compiled_path)

        # Collect css files
        if self._is_css(path):
          css.add(compiled_path)

        # Collect to be gzipped files
        if is_gzip and not self._is_image(path):
          gzipped.add(compiled_path)
        else:
          raw.add(compiled_path)

        # Copy to compile path
        shutil.copy(path, os.path.join(self._tmpdir, compiled_path))
        compiled.add(compiled_path)

        # Memoize
        self._compiled_paths[self._key(
          # NOTE: Path is relative to static folder
          os.path.relpath(path, self._app.static_folder),
          is_gzip,
        )] = compiled_path

        self._logger.debug('Compiled: %r -> %r', path, compiled_path)

    # Fix CSS paths
    for compiled_path in css:
      output = os.path.join(self._tmpdir, compiled_path)
      with open(output, 'rb') as f:
        data = f.read()
      is_gzip = '/gz/' in compiled_path
      with open(output, 'wb') as f:
        f.write(self._fix_css(data, is_gzip))

    # Gzip files
    for compiled_path in gzipped:
      output = os.path.join(self._tmpdir, compiled_path)
      with open(output, 'rb') as f:
        data = f.read()
      fgz = gzip.open(output, 'wb')
      fgz.write(data)
      fgz.close()

    compiled_count = dict(
      all=len(compiled),
      css=len(css),
      images=len(images),
      gzip=len(gzipped),
      raw=len(raw),
    )

    self._logger.info("Compiled: %r", compiled_count)

    return compiled

  def _upload(self, path, bucket, headers, key_prefix, overwrite):
    try:
      key_name = key_prefix + path
      key = bucket.get_key(key_name)
      if key and not overwrite:
        self._logger.info("Already exists: %r", path)
        return False
      else:
        key = bucket.new_key(key_name)
        key.set_contents_from_filename(
          os.path.join(self._tmpdir, path),
          headers=headers,
        )
        key.set_acl('public-read')
        self._logger.debug("Uploaded: %r", path)
        return True

    except Exception:
      self._logger.error("Failed to upload: %r", path)
      raise

  def _build_url(self, path):
    path = self._key_prefix + path
    if self._cdn_host:
      return "%s://%s/%s" % (self._scheme, self._cdn_host, path)
    else:
      return self._calling_format.build_url_base(
        self._conn,
        self._scheme,
        S3Connection.DefaultHost,
        self._bucket_name,
        path,
      )

  def init_app(self, app):
    self._app = app

    self._access_key_id = app.config['UPSTATIC_S3_ACCESS_KEY_ID']
    self._secret_access_key = app.config['UPSTATIC_S3_SECRET_ACCESS_KEY']
    self._bucket_name = app.config['UPSTATIC_S3_BUCKET_NAME']

    self._key_prefix = app.config.get('UPSTATIC_S3_KEY_PREFIX', '')
    self._cdn_host = app.config.get('UPSTATIC_S3_CDN_HOST')
    self._scheme = app.config.get('UPSTATIC_SCHEME', 'http')

    self._calling_format = OrdinaryCallingFormat()

    self._conn = S3Connection(self._access_key_id, self._secret_access_key)
    self._tmpdir = mkdtemp()

    self._logger = logging.getLogger(__name__) or logging.root

    if not self.use_local:
      self.compile()

  def url_for(self, *args, **kwargs):
    if self.use_local or not args[0].endswith('static'):
      return _url_for(*args, **kwargs)

    # Normalize path
    path = kwargs['filename'].strip('/')

    # Get headers info
    is_gzip = (
      'gzip' in request.headers.get('Accept-Encoding', '') and
      not self._is_image(path)
    )

    # Get compiled path
    compiled_path = self._compiled_paths[self._key(path, is_gzip)]

    return self._build_url(compiled_path)

  def upload(self, overwrite=False):
    self._logger.info("Uploading...")

    bucket = self._conn.create_bucket(self._bucket_name)
    key_prefix = self._key_prefix
    headers = {
      'Cache-Control': 'max-age=31556926',  # 1 year
    }
    uploaded = dict(
      raw=0,
      gzip=0,
    )
    for compiled_path in self._compiled_paths.values():
      is_gzip = '/gz/' in compiled_path

      if is_gzip:
        headers['Content-Encoding'] = 'gzip'
      else:
        headers.pop('Content-Encoding', None)
      headers['Content-Type'] = (
        mimetypes.guess_type(compiled_path)[0] or
        'application/octet-stream'
      )

      if self._upload(
          compiled_path,
          bucket,
          headers,
          key_prefix,
          overwrite,
        ):
        uploaded['raw'] += not is_gzip
        uploaded['gzip'] += is_gzip

    self._logger.info("Uploaded: %r", uploaded)

