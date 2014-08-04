import sys
import json
import h5py as h5


def get_handles():
    '''
    Reading "handles" from standard input as JSON.
    '''
    handles = json.loads(sys.stdin.read())

    return handles


def read_input_args(handles):
    '''
    Reading input arguments from HDF5 file
    using the location specified in "handles".
    '''

    hdf5_root = h5.File(handles['hdf5_filename'], 'r')

    input_args = dict()
    for key in handles['input_keys']:
        location = handles['input_keys'][key]
        input_args[key] = hdf5_root[location]

    return input_args


def write_output_args(handles, output_args):
    '''
    Writing output arguments to HDF5 file
    using the location specified in "handles".
    '''

    hdf5_root = h5.File(handles['hdf5_filename'], 'r')

    for key in output_args:
        location = handles['output_keys'][key]
        hdf5_root.create_dataset(location, data=output_args[key])
