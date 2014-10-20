import os
import sys
import json
import errno

SQL_PATH = 'sql'
SETTINGS_FILENAME = 'settings.json'

def make_directory(path):
    """ makes a directory, checking if it exists first
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise FileExistsError


def setup(sql_path, settings_filename, site_names):
    """ sets up the directory structure and settings file template
    """
    # make the directory structure
    make_directory(sql_path)
    # make a default site if the site names are blank
    if len(site_names) == 0:
        site_names = ['main']
    for site_name in site_names:
        make_directory(os.path.join(SQL_PATH, site_name))

    # add the settings file
    settings_template = {'sites': {s: {'db_driver': '<python module name>',
                                       'db_connection_string': '<database connection string>'}
                                   for s in site_names},
                         'website_title': 'qRequest',
                         'website_description': 'Run some queries',
                         'website_port_number': 5000}

    with open(os.path.join(sql_path, settings_filename), 'w') as f:
        json.dump(settings_template, f, indent=4, sort_keys=True)


def run():
    """ runs the site
    """
    from . import webserver as ws

    ws.app.run(host='0.0.0.0', port=ws.settings['website_port_number'], debug=False)


def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        command = None
    args = sys.argv[2:]

    if command == 'setup':
        setup(SQL_PATH, SETTINGS_FILENAME, args)

    elif command == 'run':
        run()

    else:
        print("Usage:\n\tqrequest.py setup [site1, site2, ...]\n\tqrequest.py run")