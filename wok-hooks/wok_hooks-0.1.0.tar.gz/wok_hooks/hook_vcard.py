import logging
import vobject
import os
import json
import gnupg


def add_vcard_to_contact(config):
    for dirpath, _, filenames in os.walk(config['media_dir']):
        for filename in filenames:
            with open(os.path.join(dirpath, filename), 'rb') as file_handle:
                if file_handle.readline().strip() == 'BEGIN:VCARD':
                    file_handle.seek(0)
                    v = vobject.readOne(file_handle)

                    name = v.fn.value
                    email = v.email.value
                    uris = []
                    if 'x-uris' in v.contents:
                        for uri in v.contents['x-uris']:
                            short_title = uri.value.split('/')[2]
                            uris.append((short_title, uri.value))

                    gpg_key = None
                    gpg_path = os.path.join(dirpath, '.'.join((filename.split('.')[:-1])) + '.asc')
                    if os.path.exists(gpg_path):

                        gpg = gnupg.GPG()
                        key_data = open(gpg_path).read()
                        keyfile = gpg.import_keys(key_data)
                        fingerprint = keyfile.results[0]['fingerprint']

                        if gpg_path.startswith(os.sep):
                            gpg_path = gpg_path[len(os.sep):]
                        if gpg_path.startswith(config['media_dir']):
                            gpg_path = gpg_path[len(config['media_dir']):]
                        gpg_key = fingerprint, gpg_path

                    meta_data = [
                        ('title', name),
                        ('type', 'contact'),
                        ('category', 'contact'),
                        ('name', name),
                        ('email', email)
                    ]

                    if gpg_key:
                        meta_data.append(('gpg', gpg_key))

                    if uris:
                        meta_data.append(('links', uris))

                    new_filename = filename.split('.')[:-1]
                    new_filename.append('md')
                    new_filename = '.'.join(new_filename)

                    new_path = os.path.sep.join([config['content_dir'], 'contact', new_filename])

                    with open(new_path, 'wb') as new_file_handle:
                        for key, value in meta_data:
                            if not isinstance(value, basestring):
                                value = json.dumps(value)
                            new_file_handle.write('%s: %s\n' % (key, value))
                        new_file_handle.writelines('---\n')


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s:%(message)s', level=logging.DEBUG)
    add_vcard_to_contact({})