"""Utilities for comparing HDF5 databases."""
import h5py


def compare_hdf5(a, b):
    """Recursively compare all entries of an HDF5 database."""
    assert type(a) == type(b), 'Type mismatch at %s: %s != %s' % (
        a, type(a), type(b))

    a_attrs = dict(a.attrs.items())
    b_attrs = dict(b.attrs.items())
    assert a_attrs == b_attrs, 'Attribute mismatch at %s: %s != %s' % (
        a, a_attrs, b_attrs)

    if isinstance(a, h5py.Dataset):
        assert len(a) == len(b), 'Entry count mismatch at %s: %s != %s' % (
            a, len(a), len(b))

        if len(a) == 0:
            # Empty datasets cannot be accessed.
            return

        a_values = a[:].tolist()
        b_values = b[:].tolist()

        assert a_values == b_values, 'Dataset mismatch at %s: %s != %s' % (
            a, a_values, b_values)
    else:
        assert set(a.keys()) == set(b.keys()), 'Group mismatch at %s: %s' % (
            a, ', '.join(sorted(set(a.keys()) ^ set(b.keys()))))

        for name in sorted(a.keys()):
            compare_hdf5(a[name], b[name])

    return True
