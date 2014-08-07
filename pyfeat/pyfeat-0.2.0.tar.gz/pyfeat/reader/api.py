r"""
.. moduleauthor:: Christoph Wehmeyer <christoph.wehmeyer@fu-berlin.de>

This is the API function to read suitably formatted files to create a data object for further analysis: ::

   from pyfeat import read_files
   data = read_files( [ 'file_1', 'file_2', ..., 'file_n' ] )

"""

from .reader import Reader

def read_files( files, kT_file=None, wham_file=None, kT_target=None, maxlength=None, stride=1, skiprows=0, verbose=False ):
    r"""
    API function for reading files and creating the data object
    
    Parameters
    ----------
    files : list of strings
    	file names to read
    kT_file : string (optional)
    	file name for kT value listing
    wham_file : string (optional)
    	file name for wham data
    kT_target : float (optional)
        target temperature ( uses lowest kT if not given)
    maxlength : int (optional)
    	specify the maximal number of frames when reading the trajectory files
    stride : int (optional)
    	specify the stride when reading the trajectory files
    skiprows : int (optional)
    	specify the number of skipped lines when reading the trajectory files
    verbose : boolean (optional)
    	verbose output during the reading/building process
    
    Returns
    -------
    data : pyfeat.data.Data object
    	information container for further analysis
    """
    reader = Reader( files, kT_file=kT_file, wham_file=wham_file, kT_target=kT_target, maxlength=maxlength, stride=stride, skiprows=skiprows, verbose=verbose )
    return reader.build_data_object()
