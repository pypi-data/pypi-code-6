#------------------------------------------------------------------------------
# ABOUT NLMpy.py
#------------------------------------------------------------------------------

# NLMpy is a Python package for the creation of neutral landscape models that
# are widely used in the modelling of ecological patterns and processes across
# landscapes.

# A full description of NLMpy is published in: Etherington et al. (2014) NLMpy:
# a Python software package for the creation of neutral landscape models within
# a general numerical framework. X, X: X-X.

# All code is copyright 2014 Thomas R. Etherington, E. Penelope Holland, and
# David O'Sullivan.

# This work is licensed under the Creative Commons Attribution-NonCommercial-
# ShareAlike 3.0 License.  To view a copy of this license, visit 
# http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to 
# Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.

#------------------------------------------------------------------------------

import math
import numpy as np
from scipy import ndimage

#------------------------------------------------------------------------------
# REQUIRED FUNCTIONS:
#------------------------------------------------------------------------------

def linearRescale01(array):
    """    
    A rescale in which the values in the array are linearly rescaled to range
    between 0 and 1.

    Parameters
    ----------
    array : array
        2D array of data values.
        
    Returns
    -------
    out : array
        2D array with rescaled values.
    """
    rescaledArray = (array - np.nanmin(array)) / np.nanmax(array - np.nanmin(array))
    return(rescaledArray)

#------------------------------------------------------------------------------

# A function to insert nan cells into an array based on a binary mask array.
def maskArray(array, maskArray):
    """    
    Return the array with nan values inserted where present in the mask array.
    It is assumed that both the arrays have the same dimensions.

    Parameters
    ----------
    array : array
        2D array of data values.
    maskArray : array
        2D array used as a binary mask.
        
    Returns
    -------
    out : array
        2D array with masked values.
    """
    np.place(array, maskArray==0, np.nan)
    return(array)

#------------------------------------------------------------------------------

def randomUniform01(nRow, nCol, mask=None):
    """    
    Create an array with random values ranging 0-1.

    Parameters
    ----------
    nRow : int
        The number of rows in the array.
    nCol : int
        The number of columns in the array.
    mask : array, optional
        2D array used as a binary mask to limit the elements with values.
        
    Returns
    -------
    out : array
        2D float array.
    """
    if mask is None:
        mask = np.ones((nRow, nCol))
    array = np.random.random((nRow, nCol))
    maskedArray = maskArray(array, mask)
    rescaledArray = linearRescale01(maskedArray)
    return(rescaledArray)
    
#------------------------------------------------------------------------------

def nnInterpolate(array, missing):
    """    
    Two-dimensional array nearest-neighbour interpolation in which the elements
    in the positions indicated by the array "missing" are replaced by the
    nearest value from the "array" of data values.

    Parameters
    ----------
    array : array
        2D array of data values.
    missing: boolean array
        Values of True receive interpolated values.
        
    Returns
    -------
    out : array
        2D array with interpolated values.
    """
    # Get row column based index of nearest value
    rcIndex = ndimage.distance_transform_edt(missing, return_distances=False, 
                                             return_indices=True)
    # Create a complete array by extracting values based on the index
    interpolatedArray = array[tuple(rcIndex)]
    return(interpolatedArray)

#------------------------------------------------------------------------------

def w2cp(weights):
    """    
    Convert a list of category weights into a 1D NumPy array of cumulative 
    proportions.

    Parameters
    ----------
    weights : list
        A list of numeric values
        
    Returns
    -------
    out : array
        1D array of class cumulative proportions.
    """
    w = np.array(weights, dtype=float)
    proportions = w / np.sum(w)
    cumulativeProportions = np.cumsum(proportions)
    cumulativeProportions[-1] = 1 # to ensure the last value is 1
    return(cumulativeProportions)

#------------------------------------------------------------------------------

def calcBoundaries(array, cumulativeProportions, classifyMask=None):
    """    
    Determine upper class boundaries for classification of an array with values
    ranging 0-1 based upon an array of cumulative proportions.

    Parameters
    ----------
    array : array
        2D array of data values.
    cumulativeProportions : array
        1D array of class cumulative proportions.
    classifyMask : array, optional
        2D array used as a binary mask to limit the elements used to determine
        the upper boundary values for each class.
        
    Returns
    -------
    out : array
        1D float array.
    """
    if classifyMask is None:
        classifyMask = np.ones(np.shape(array))
    maskedArray = array * classifyMask
    np.place(maskedArray, classifyMask==0, np.nan)
    # Determine the number of cells that are in the classification mask.
    nCells = np.count_nonzero(np.isfinite(maskedArray))
    # Based on the number of cells, find the index of upper boundary element
    boundaryIndexes = (cumulativeProportions * nCells).astype(int) - 1
    # Index out the the upper boundary value for each class
    boundaryValues = np.sort(np.ndarray.flatten(maskedArray))[boundaryIndexes]
    # Ensure the maximum boundary value is equal to 1
    boundaryValues[-1] = 1
    return(boundaryValues)

#------------------------------------------------------------------------------
      
def classifyArray(array, weights, classifyMask=None):
    """    
    Classify an array with values ranging 0-1 into proportions based upon a 
    list of class weights.

    Parameters
    ----------
    array : array
        2D array of data values.
    weights : list
        A list of numeric values
    classifyMask : array, optional
        2D array used as a binary mask to limit the elements used to determine
        the upper boundary values for each class.
        
    Returns
    -------
    out : array
        2D array.
    """
    cumulativeProportions = w2cp(weights)
    boundaryValues = calcBoundaries(array, cumulativeProportions, classifyMask)
    # Classify the array
    classifiedArray = np.searchsorted(boundaryValues, array)
    # Replace any nan values
    classifiedArray = classifiedArray.astype(float)
    np.place(classifiedArray, np.isnan(array), np.nan)
    return(classifiedArray)

#------------------------------------------------------------------------------

def blendArray(primaryArray, arrays, scalingFactors=None):
    """    
    Blend a primary array with other arrays weighted by scaling factors.

    Parameters
    ----------
    primaryArray : array
        2D array of data values.
    arrays : list
        List of 2D arrays of data values.
    scalingFactors : list
        List of scaling factors used to weight the arrays in the blend.
        
    Returns
    -------
    out : array
        2D array.
    """
    if scalingFactors is None:
        scalingFactors = np.ones(len(arrays))
    for n in range(len(arrays)):
        primaryArray = primaryArray + (arrays[n] * scalingFactors[n])
    blendedArray = primaryArray / len(arrays)
    rescaledArray = linearRescale01(blendedArray)
    return(rescaledArray)
    
#------------------------------------------------------------------------------

def blendClusterArray(primaryArray, arrays, scalingFactors=None):
    """    
    Blend a primary cluster NLM with other arrays in which the mean value per 
    cluster is weighted by scaling factors.

    Parameters
    ----------
    primaryArray : array
        2D array of data values in which values are clustered.
    arrays : list
        List of 2D arrays of data values.
    scalingFactors : list
        List of scaling factors used to weight the arrays in the blend.
        
    Returns
    -------
    out : array
        2D array.
    """
    if scalingFactors is None:
        scalingFactors = np.ones(len(arrays))
    for n in range(len(arrays)):
        meanOfClusterArray = meanOfCluster(primaryArray, arrays[n])
        primaryArray = primaryArray + (meanOfClusterArray * scalingFactors[n])
    blendedArray = primaryArray / len(arrays)
    rescaledArray = linearRescale01(blendedArray)
    return(rescaledArray)
    
#------------------------------------------------------------------------------

def meanOfCluster(clusterArray, array):
    """    
    For each cluster of elements in an array, calculate the mean value for the
    cluster based on a second array.

    Parameters
    ----------
    clutserArray : array
        2D array of data values in which values are clustered.
    array : array
        2D array of data values.
        
    Returns
    -------
    out : array
        2D array.
    """
    meanClusterValues = np.zeros(np.shape(clusterArray))
    clusterValues = np.unique(clusterArray)
    for value in clusterValues:
        if np.isfinite(value):
            # Extract location of values
            valueLocs = clusterArray == value
            # Define clusters in array
            clusters, nClusters = ndimage.measurements.label(valueLocs)
            # Get mean for each cluster
            means = ndimage.mean(array, clusters, range(1,nClusters + 1))
            means = np.insert(means, 0, 0) # for background non-cluster
            # Apply mean values to clusters by index
            clusterMeans = means[clusters]
            # Add values for those clusters to array
            meanClusterValues = meanClusterValues + clusterMeans
    np.place(meanClusterValues, np.isnan(clusterArray), np.nan)
    rescaledArray = linearRescale01(meanClusterValues)
    return(rescaledArray)
    
#------------------------------------------------------------------------------
# NEUTRAL LANDSCAPE MODELS:
#------------------------------------------------------------------------------

def random(nRow, nCol, mask=None):
    """    
    Create a spatially random neutral landscape model with values ranging 0-1.

    Parameters
    ----------
    nRow : int
        The number of rows in the array.
    nCol : int
        The number of columns in the array.
    mask : array, optional
        2D array used as a binary mask to limit the elements with values.
        
    Returns
    -------
    out : array
        2D array.
    """
    array = randomUniform01(nRow, nCol, mask)
    return(array)
    
#------------------------------------------------------------------------------

def planarGradient(nRow, nCol, direction=None, mask=None):
    """    
    Create a planar gradient neutral landscape model with values ranging 0-1.

    Parameters
    ----------
    nRow : int
        The number of rows in the array.
    nCol : int
        The number of columns in the array.
    direction: int, optional
        The direction of the gradient as a bearing from north, if unspecified
        the direction is randomly determined.
    mask : array, optional
        2D array used as a binary mask to limit the elements with values.
        
    Returns
    -------
    out : array
        2D array.
    """
    if direction is None:
        direction = np.random.uniform(0, 360, 1) # a random direction
    if mask is None:
        mask = np.ones((nRow, nCol))
    # Create arrays of row and column index
    rowIndex, colIndex = np.indices((nRow, nCol))
    # Determine the eastness and southness of the direction
    eastness = np.sin(np.deg2rad(direction))
    southness = np.cos(np.deg2rad(direction)) * -1
    # Create gradient array
    gradientArray = (southness * rowIndex + eastness * colIndex)
    maskedArray = maskArray(gradientArray, mask)
    rescaledArray = linearRescale01(maskedArray)
    return(rescaledArray)

#------------------------------------------------------------------------------

def edgeGradient(nRow, nCol, direction=None, mask=None):
    """    
    Create an edge gradient neutral landscape model with values ranging 0-1.

    Parameters
    ----------
    nRow : int
        The number of rows in the array.
    nCol : int
        The number of columns in the array.
    direction: int, optional
        The direction of the gradient as a bearing from north, if unspecified
        the direction is randomly determined.
    mask : array, optional
        2D array used as a binary mask to limit the elements with values.
        
    Returns
    -------
    out : array
        2D array.
    """
    # Create planar gradient
    gradientArray = planarGradient(nRow, nCol, direction, mask)
    # Transform to a central gradient
    edgeGradientArray = (np.abs(0.5 - gradientArray) * -2) + 1
    rescaledArray = linearRescale01(edgeGradientArray)
    return(rescaledArray)

#------------------------------------------------------------------------------

def distanceGradient(source, mask=None):
    """    
    Create a distance gradient neutral landscape model with values ranging 0-1.

    Parameters
    ----------
    source : array
        2D array binary array that defines the source elements from which
        distance will be measured.  The dimensions of source also specify
        the output dimensions of the distance gradient.
    mask : array, optional
        2D array used as a binary mask to limit the elements with values.
        
    Returns
    -------
    out : array
        2D array.
    """
    if mask is None:
        mask = np.ones(np.shape(source))
    gradient = ndimage.distance_transform_edt(1 - source)
    maskedArray = maskArray(gradient, mask)
    rescaledArray = linearRescale01(maskedArray)
    return(rescaledArray)

#------------------------------------------------------------------------------

def mpd(nRow, nCol, h, mask=None):
    """    
    Create a midpoint displacement neutral landscape model with values ranging 
    0-1.

    Parameters
    ----------
    nRow : int
        The number of rows in the array.
    nCol : int
        The number of columns in the array.
    h: float
        The h value controls the level of spatial autocorrelation in element
        values.
    mask : array, optional
        2D array used as a binary mask to limit the elements with values.
        
    Returns
    -------
    out : array
        2D array.
    """
    if mask is None:
        mask = np.ones((nRow, nCol))  
    # Determine the dimension of the smallest square
    maxDim = max(nRow, nCol)
    N = int(math.ceil(math.log(maxDim - 1, 2)))
    dim = 2 ** N + 1
    # Create a surface consisting of random displacement heights average value
    # 0, range from [-0.5, 0.5] x displacementheight
    disheight = 2.0
    surface = np.random.random([dim,dim]) * disheight -0.5 * disheight
    
    #--------------------------------------------------------------------------
    
    # Apply the square-diamond algorithm
    def randomdisplace(disheight):
        # Returns a random displacement between -0.5 * disheight and 0.5 * disheight
        return np.random.random() * disheight -0.5 * disheight
    
    def displacevals(p, disheight):
        # Calculate the average value of the 4 corners of a square (3 if up
        # against a corner) and displace at random.
        if len(p) == 4:
            pcentre = 0.25 * sum(p) + randomdisplace(disheight)
        elif len(p) == 3:
            pcentre = sum(p) / 3 + randomdisplace(disheight)	
        return pcentre
    
    def check_diamond_coords(diax,diay,dim,i2):
        # get the coordinates of the diamond centred on diax, diay with radius i2
        # if it fits inside the study area
        if diax < 0 or diax > dim or diay <0 or diay > dim:
            return []
        if diax-i2 < 0:
            return [(diax+i2,diay),(diax,diay-i2),(diax,diay+i2)]
        if diax + i2 >= dim:
            return [(diax-i2,diay),(diax,diay-i2),(diax,diay+i2)]
        if diay-i2 < 0:
            return [(diax+i2,diay),(diax-i2,diay),(diax,diay+i2)]
        if diay+i2 >= dim:
            return [(diax+i2,diay),(diax-i2,diay),(diax,diay-i2)]
        return [(diax+i2,diay),(diax-i2,diay),(diax,diay-i2),(diax,diay+i2)]

    # Set square size to cover the whole array
    inc = dim-1
    while inc > 1: # while considering a square/diamond at least 2x2 in size
            
            i2 = inc/2 # what is half the width (i.e. where is the centre?)
            # SQUARE step
            for x in range(0,dim-1,inc):
                    for y in range(0,dim-1,inc):
                            # this adjusts the centre of the square 
                            surface[x+i2,y+i2] = displacevals([surface[x,y],surface[x+inc,y],surface[x+inc,y+inc],surface[x,y+inc]],disheight)
            
            # DIAMOND step
            for x in range(0, dim-1, inc):
                for y in range(0, dim-1,inc):
                    diaco = check_diamond_coords(x+i2,y,dim,i2)
                    diavals = []
                    for co in diaco:
                        diavals.append(surface[co])
                    surface[x+i2,y] = displacevals(diavals,disheight)
                   
                    diaco = check_diamond_coords(x,y+i2,dim,i2)
                    diavals = []
                    for co in diaco:
                        diavals.append(surface[co])
                    surface[x,y+i2] = displacevals(diavals,disheight)

                    diaco = check_diamond_coords(x+inc,y+i2,dim,i2)
                    diavals = []
                    for co in diaco:
                        diavals.append(surface[co])
                    surface[x+inc,y+i2] = displacevals(diavals,disheight)

                    diaco = check_diamond_coords(x+i2,y+inc,dim,i2)
                    diavals = []
                    for co in diaco:
                        diavals.append(surface[co])
                    surface[x+i2,y+inc] = displacevals(diavals,disheight)
                    
            # Reduce displacement height
            disheight = disheight * 2 ** (-h)
            inc = inc / 2

    #--------------------------------------------------------------------------
    
    # Extract a portion of the array to match the dimensions
    randomStartRow = np.random.choice(range(dim - nRow))
    randomStartCol = np.random.choice(range(dim - nCol))
    array = surface[randomStartRow:randomStartRow + nRow,
                    randomStartCol:randomStartCol + nCol]
    # Apply mask and rescale 0-1
    maskedArray = maskArray(array, mask)
    rescaledArray = linearRescale01(maskedArray)
    return(rescaledArray)
    
#------------------------------------------------------------------------------

def randomRectangularCluster(nRow, nCol, minL, maxL, mask=None):
    """    
    Create a random rectangular cluster neutral landscape model with 
    values ranging 0-1.

    Parameters
    ----------
    nRow : int
        The number of rows in the array.
    nCol : int
        The number of columns in the array.
    minL: int
        The minimum possible length of width and height for each random 
        rectangular cluster.
    maxL: int
        The maximum possible length of width and height for each random 
        rectangular cluster.
    mask : array, optional
        2D array used as a binary mask to limit the elements with values.
        
    Returns
    -------
    out : array
        2D array.
    """    
    if mask is None:
        mask = np.ones((nRow, nCol))
    # Create an empty array of correct dimensions
    array = np.zeros((nRow, nCol)) - 1
    # Keep applying random clusters until all elements have a value
    while np.min(array) == -1:
        width = np.random.choice(range(minL, maxL))
        height = np.random.choice(range(minL, maxL))
        row = np.random.choice(range(-maxL, nRow))
        col = np.random.choice(range(-maxL, nCol))
        array[row:row + width, col:col + height] = np.random.random()   
    # Apply mask and rescale 0-1        
    maskedArray = maskArray(array, mask)
    rescaledArray = linearRescale01(maskedArray)
    return(rescaledArray)

#------------------------------------------------------------------------------

def randomElementNN(nRow, nCol, n, mask=None):
    """    
    Create a random element nearest-neighbour neutral landscape model with 
    values ranging 0-1.

    Parameters
    ----------
    nRow : int
        The number of rows in the array.
    nCol : int
        The number of columns in the array.
    n: int
        The number of elements randomly selected to form the basis of
        nearest-neighbour clusters.
    mask : array, optional
        2D array used as a binary mask to limit the elements with values.
        
    Returns
    -------
    out : array
        2D array.
    """
    if mask is None:
        mask = np.ones((nRow, nCol))
    # Create an empty array of correct dimensions
    array = np.zeros((nRow, nCol))
    # Insert value for n elements
    for element in range(n):
        randomRow = np.random.choice(range(nRow))
        randomCol = np.random.choice(range(nCol))
        if array[randomRow, randomCol] == 0 and mask[randomRow, randomCol] == 1:
            array[randomRow, randomCol] = np.random.random(1)
    # Interpolate the values
    interpolatedArray = nnInterpolate(array, array==0)
    # Apply mask and rescale 0-1
    maskedArray = maskArray(interpolatedArray, mask)
    rescaledArray = linearRescale01(maskedArray)
    return(rescaledArray)
 
#------------------------------------------------------------------------------

def randomClusterNN(nRow, nCol, p, n='4-neighbourhood', mask=None):
    """    
    Create a random cluster nearest-neighbour neutral landscape model with 
    values ranging 0-1.

    Parameters
    ----------
    nRow : int
        The number of rows in the array.
    nCol : int
        The number of columns in the array.
    p: float
        The p value controls the proportion of elements randomly selected to
        form clusters.
    n: string, optional
        Clusters are defined using a set of neighbourhood structures that 
        include:
                            [0,1,0]
        '4-neighbourhood' = [1,1,1]
                            [0,1,0]
                            
                            [1,1,1]
        '8-neighbourhood' = [1,1,1]
                            [1,1,1]
                            
                     [0,1,1]
        'diagonal' = [1,1,1]
                     [1,1,0]
                     
        The default parameter setting is '4-neighbourhood'.
        
    mask : array, optional
        2D array used as a binary mask to limit the elements with values.
        
    Returns
    -------
    out : array
        2D array.
    """
    if mask is None:
        mask = np.ones((nRow, nCol))
    # Define a dictionary of possible neighbourhood structures:
    neighbourhoods = {}
    neighbourhoods['4-neighbourhood'] = np.array([[0,1,0],
                                                  [1,1,1],
                                                  [0,1,0]])
    neighbourhoods['8-neighbourhood'] = np.array([[1,1,1],
                                                  [1,1,1],
                                                  [1,1,1]])
    neighbourhoods['diagonal'] = np.array([[0,1,1],
                                           [1,1,1],
                                           [1,1,0]])
    # Create percolation array
    randomArray = random(nRow, nCol, mask)
    percolationArray = classifyArray(randomArray, [1 - p, p])
    # As nan not supported in cluster algorithm replace with zeros
    np.place(percolationArray, np.isnan(percolationArray), 0)
    # Define clusters
    clusters, nClusters = ndimage.measurements.label(percolationArray, 
                                                     neighbourhoods[n])
    # Create random set of values for each the clusters
    randomValues = np.random.random(nClusters)
    randomValues = np.insert(randomValues, 0, 0) # for background non-cluster
    # Apply values by indexing by cluster
    clusterArray = randomValues[clusters]
    # Gap fill with nearest neighbour interpolation
    interpolatedArray = nnInterpolate(clusterArray, clusterArray==0)
    # Apply mask and rescale 0-1
    maskedArray = maskArray(interpolatedArray, mask)
    rescaledArray = linearRescale01(maskedArray)
    return(rescaledArray)

#------------------------------------------------------------------------------
