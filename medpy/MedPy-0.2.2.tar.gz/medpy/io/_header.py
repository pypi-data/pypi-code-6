"""
@package medpy.io.header
The MedPy header classes for wrapping the headers of the various 3rd party tools.
Provides functionality to access the image information in a standardized way.

The supplied methods hide more complex usage of a number of third party modules.

@author Oskar Maier
@version r0.1.0
@since 2013-05-23
@status Development
"""

# build-in modules

# third-party modules
import numpy

# own modules

# code
def factory_by_image(third_party_image):
    """
    Returns the appropriate initialized version of the MedPy header for the supplied
    third party image.
    
    @param third_party_image an image loaded through a 3rd party module
    """
    pass
    
def factory_by_filename(image_filename):
    """
    Returns the appropriate (empty) version of the MedPy header for the supplied
    image type.
    
    @param image_filename an image filename of a supported image file type that will
                          be indentified by its ending
    """
    pass

class ImageHeader(object):
    """The abstract MedPy image header base class."""
    
    """The voxel spacing."""
    _spacing = None
    """The offset (in real-world units, usually mm, sometimes also time for the 4th dimension)."""
    _offset = None
    """The shape of the image data."""
    _shape = None
    """The data type of the image voxels (as numpy.dtype)."""
    _dtype = None
    
    def __init__(self):
        """
        Do not call this directly.
        The child classes are required to set the membership variables or to override
        the getters/setters when calculating them directly.
        """
        raise NotImplementedError( "The class is abstract and not meant to be used directly." )
    
    # PUBLIC
    def update_by_header(self, hdr):
        """
        Update all of this headers data fields by copying the values from the supplied
        header.
        
        @param hdr a ImageHeader instance
        """
        self.set_spacing( hdr.get_spacing() )
        self.set_offset( hdr.get_spacing() )
        # !TODO: This should not be set, but read from the array!
        self._set_shape( hdr.get_shape() )
        self._set_dtype( hdr.dtype() )

    # GETTER
    def get_spacing(self):
        """@return the voxel spacing"""
        return self._spacing

    def get_offset(self):
        """
        @return the offset (in real-world units, usually mm, sometimes also time for the
                4th dimension) of the first voxels center point
        """ 
        return self._offset

    def get_shape(self):
        """@return the shape of the image"""
        return self._shape

    def get_dtype(self):
        """@return the voxel data type of the image as numpy.dtype"""
        return self._dtype
    
    def get_dimensionality(self):
        """@return the number of image dimensions"""
        return len(self._shape)
    
    # SETTER
    def set_spacing(self, value):
        """
        @param value a one dimensional sequence with as many elements as the image has
                     dimensions 
        """
        self._spacing = numpy.asarray(value)

    def set_offset(self, value):
        """
        @param value a one dimensional sequence with as many elements as the image has
                     dimensions
        """
        self._offset = numpy.asarray(value)
    
    # PROTECTED / PRIVATE
    def _set_shape(self, value):
        """
        @param value the new shape of the array
        """
        self._shape = numpy.asarray(value)
        
    def _set_dtype(self, value):
        """
        @param value the new data type of the array
        @raise TypeError if the data type could not beconverted to a numpy.dtype
        """
        self._shape = numpy.dtype(value)
    
    
    
        