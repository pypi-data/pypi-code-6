

# EMAIL_BACKEND = 'appengine_utils.mail.AsyncEmailBackend'  # use on production
EMAIL_BACKEND = 'appengine_utils.mail.EmailBackend'
# Specify a queue name for the async. email backend.
EMAIL_QUEUE_NAME = 'default'


PREPARE_UPLOAD_BACKEND = 'appengine_utils.storage.prepare_upload'
SERVE_FILE_BACKEND = 'appengine_utils.storage.serve_file'
DEFAULT_FILE_STORAGE = 'appengine_utils.storage.BlobstoreStorage'
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024
FILE_UPLOAD_HANDLERS = (
    'appengine_utils.storage.BlobstoreFileUploadHandler',
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'TIMEOUT': 0,
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
