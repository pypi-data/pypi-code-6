import glob
from os.path import basename

def sync_keys():
    local_keys = dict((basename(path), open(path).read()) for path in glob.glob('keys/*'))
    registered_keys = dict((key['name'], key) for key in client.keys.list().result['ssh_keys'])
    local_key_names = set(local_keys.keys())
    registered_key_names = set(registered_keys.keys())
    new_key_names = local_key_names.difference(registered_key_names)
    keynames_to_discard = registered_key_names.difference(local_keys)
    for name in new_key_names:
        client.keys.create(name=name, public_key=local_keys[name])
    for name in keynames_to_discard:
        client.keys.delete(registered_keys[name]['id'])
    return {'new': new_key_names, 'deleted': keynames_to_discard, 'all_ids': [key['id'] for key in registered_keys.values()]}



