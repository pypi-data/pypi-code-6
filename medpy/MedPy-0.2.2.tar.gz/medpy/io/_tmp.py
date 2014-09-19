#Nibabel with nifti or analyze



realshape = numpy.squeeze(img.get_shape()) # required for loading dicom and analyze
hdr = img.get_header()
# Returns the offset (presumably in mm, probably s for the last dimension when time)
offset = [hdr['qoffset_x'], hdr['qoffset_y'], hdr['qoffset_z'], hdr['toffset']][0:len(realshape)] # in world coordinate system (mm)
# Returns the voxels spacings
spacing = img.get_header().get_zooms()[0:len(realshape)]
# Returns the data shape
shape = realshape
# Returns the data type as numpy.dtype
dtype = img.get_data_dtype()
# To translate a voxel-index to to the real-world (or something like this) coordination system
img.get_affine().dot(numpy.append(index, 0))

# PyDicom
shape = img.pixel_array.shape # note: strangely the slices are the first
dtype = img.pixel_array.dtype # not really reliable, or?
spacing = numpy.append(numpy.asarray(img.PixelSpacing), float(img.SliceThickness)) # what about img.SpacingBetweenSlices?
# DICOM -> other: keep SliceThickness
# other -> DICOM: set SliceThickness = SpacingBetweenSlices
offset = img.ImagePositionPatient

#rotation = ImageOrientationPatient
# @ see: http://nipy.sourceforge.net/nibabel/dicom/dicom_orientation.html

# data -> int16, obwohl es float ist? Wird rescale-slope in pydicom nicht angewendet? Müsste Y = x * RescaleSlope + RescaleIntend sein!
# Note:  You should only deal with Rescale Slope/Intercept from MR Image Storage coming from philips system. I have not seen any other people used it in the legacy SOP instances.


# ITK
origin = img.GetOrigin()
origin.GetElement(0-origin.Size()-1) # => 89.1362075805664, -110.98018646240234, -98.8212890625
spacing = img.GetSpacing()
spacing.GetElement(0-spacing.Size()-1) # => voxel spacing
arr.dtype
arr.shape

# loading of data
#ITKSnap erkennt ob RescaleSlope oder RescaleIntend gesetzt sind und ob sie type float sind! Wenn ja, wird dementsprechend die Intensitätwerte verändert und geladen, e.g. as float!



