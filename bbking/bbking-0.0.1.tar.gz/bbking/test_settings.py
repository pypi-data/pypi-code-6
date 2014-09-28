# test settings for bbking tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'test.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

INSTALLED_APPS = (
    'bbking',
)

BBKING_TAG_LIBRARIES = (
    'bbking.bbtags.text',
    'bbking.bbtags.hrefs',
    'bbking.bbtags.quote',
    'bbking.bbtags.code',
    'bbking.bbtags.embed',
)

BBKING_USE_WORDFILTERS = True
