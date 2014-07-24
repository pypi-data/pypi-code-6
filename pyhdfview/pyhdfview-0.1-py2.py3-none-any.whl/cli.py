"""A command line HDF5 viewer.

Usage:
    hv <path>
    hv attrs <path>

<path> must be an HDF5 filename with an optional path to a HDF5 group appended,
e.g., "test.hdf5" or "test.hdf5:/path/to/group".

"""
import colorama
import docopt
import h5py


colorama.init(autoreset=True)


def print_attrs(db, path):
    attrs = db[path].attrs
    if not attrs:
        print('No attributes in %s' % pretty_path(db, path))
        return

    print('Attributes of %s' % pretty_path(db, path))
    col_width = '%%%ds' % max(len(k) for k in attrs)
    fmt_str = '• %s: %%s' % col_width
    for k, v in attrs.items():
        print(fmt_str % (k, v))


def print_dataset(db, path):
    print('Dataset %s' % pretty_path(db, path))
    print(db[path][:])


def list_children(db, path):
    print('List %s' % pretty_path(db, path))
    for item in db[path]:
        print('• %s' % item)


def split_path(path):
    if ':' not in path:
        filename, path = path, '/'
    else:
        filename, path = path.split(':', 1)
    return filename, path


def pretty_path(db, path):
    return '%s%s:%s' % (colorama.Style.BRIGHT, db.filename, path)


def main():
    arguments = docopt.docopt(__doc__)
    filename, path = split_path(arguments['<path>'])
    db = h5py.File(filename, 'r')
    if arguments['attrs']:
        print_attrs(db, path)
    else:
        if isinstance(db[path], h5py.Dataset):
            print_dataset(db, path)
        else:
            list_children(db, path)


if __name__ == '__main__':
    main()
