from ubackup import settings, log


def setup():
    log.set_config(settings.LOGGING)
    log.set_level('DEBUG')

    settings.CHUNK_SIZE = 100
    settings.CRYPT_KEY = "foo"
    settings.DROPBOX_TOKEN = "foo"
