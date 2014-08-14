from functools import reduce
import urllib.request, urllib.parse, urllib.error

import h5py
import numpy as np

MAJOR      = 1
MINOR      = 0
VERSION    = str(MAJOR) + '.' + str(MINOR)
IDENTIFIER = 'BSML ' + VERSION


#COMPRESSION = 'szip'                          #: Szip gives best performance
COMPRESSION = 'gzip'                          #: Szip gives best performance

DTYPE_STRING = h5py.special_dtype(vlen=str)   #: Store strings as variable length.




class H5Recording(object):
#=========================
  """
  Store signals as HDF5 Recordings.

  The :meth:`create` and :meth:`open` methods are intended to be used to
  create instances instead of directly using the constructor.
  """
  def __init__(self, uri, h5=None):
  #--------------------------------
    self.uri = uri
    self._h5 = h5

  def __del__(self):
  #-----------------
    self.close()


  @classmethod
  def create(cls, uri, fname, replace=False, **kwds):
  #--------------------------------------------------
    """
    Create a new HDF5 Recording file.

    :param uri: The URI of the Recording contained in the file.
    :param str fname: The name of the file to create.
    :param bool replace: If True replace any existing file (default = False).
    """
    if fname.startswith('file://'): fname = fname[7:]
    try:
      h5 = h5py.File(fname, 'w' if replace else 'w-')
    except IOError as msg:
      raise IOError("Cannot create file '%s' (%s)" % (fname, msg))
    h5.attrs['version'] = IDENTIFIER
    h5.create_group('uris')
    h5.create_group('recording')
    h5.create_group('recording/signal')
    h5['recording'].attrs['uri'] = str(uri)
    h5['uris'].attrs[str(uri)] = h5['recording'].ref
    return cls(uri, h5)


  def close(self):
  #---------------
    """
    Close a HDF5 Recording file.
    """
    if self._h5:
      self._h5.close()
      self._h5 = None


  def create_signal(self, uri, units, shape=None, data=None,
                          dtype=None, gain=None, offset=None,
                          rate=None, period=None, timeunits=None, clock=None,
                          compression=COMPRESSION, **kwds):
  #---------------------------------------------------------------------------
    if data: data = np.asarray(data)
    if data is not None:   # simple dataset, data determines shape
      npoints = len(data)
      maxshape = (None,) + data.shape[1:]
    else:                    # simple dataset, defaults
      npoints = 0
      shape = (0,)
      maxshape = (None,)

    if data is None and dtype is None:
      dtype = np.dtype('f8')      # Default to 64-bit float

    dset = self._h5['/recording/signal'].create_dataset('dataset',
        data=data, shape=shape, maxshape=maxshape, dtype=dtype,
        chunks=True) # , compression=compression)
#    dset = self._h5['/recording/signal'].create_dataset('dataset', data=data)


if __name__ == '__main__':
#=========================

  f = H5Recording.create('/some/uri', 'test.h5', True)
  f.create_signal('a signal URI', 'mV', data=[1, 2, 3], rate=10)
  f.close()

