from pkg_resources import resource_filename, resource_string


try:
    DATA_PATH = resource_filename('tlpconfig', 'data/')
    VERSION = resource_string('tlpconfig', 'VERSION')
except Exception:
    DATA_PATH = 'data/'
    with open('VERSION') as version:
        VERSION = version.read()


UI_PATH = DATA_PATH + 'ui/'
