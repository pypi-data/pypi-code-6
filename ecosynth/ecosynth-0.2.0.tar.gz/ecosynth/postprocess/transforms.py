"""
Transforms
==========

"""

__all__ = ['georef_telemetry', 'georef_telemetry_file', 'apply_helmert',
            'georef_grnd_cntrl']

import collections
import time

import numpy as np
import scipy.interpolate as sp_interpolate
import scipy.optimize as sp_optimize
import scipy.stats as sp_stats

from . import io


def georef_telemetry(out_tuple, gps_array, logger=None):
    """
    Produces a georeferenced xyzrgb_array using gps positions, the fmin_powell
    optimization algorithm, and the Helmert transform

    :param tuple out_tuple: Bundler OUT named tuple
    :param np.array gps_array: GPS positions ordered sequentially in time
    :param file logger: (Optional) Clean file to write Optimization Error Info

    :return: xyzrgb_array_transformed - georeferenced coordinates
    :rtype: np.array

    :return: parameters
    :rtype: list  [omega, phi, kappa, s, Tx, Ty, Tz]

    :raises IndexError: if such and such

    | **Notes**
    | here

    | **Example**
    | here

    """
    start = time.time()
    #  Solve Helmert
    initial_guess = [1, 1, 1, 1, 1, 1, 1]
    solution = _solve_helmert(
        initial_guess, gps_array, out_tuple.cam_array_fixed[:, 0:3], logger=logger)

    # Error Analysis
    if logger:
        _error_analysis_telem(
            solution.parameters, gps_array, out_tuple.cam_array_fixed, solution.gps_array_spline, solution.cam_array_spline, logger)

    #  Apply Helmert to Coordinates of Points
    transformed_array = apply_helmert(
        solution.parameters, out_tuple.xyzrgb_array[:, 0:3])

    #  Recombine coordinates and colors
    xyzrgb_array_transformed = np.hstack(
        (transformed_array, out_tuple.xyzrgb_array[:, 3:]))

    print "   georef_telemetry time:", time.time()-start
    return xyzrgb_array_transformed, solution.parameters


def georef_telemetry_file(out_file, gps_file, logger=None):
    """
    Produces a georeferenced xyzrgb_array using gps positions, the fmin_powell
    optimization algorithm, and the Helmert transform

    :param file out_file: Bundler OUT file
    :param file gps_file: Clean file to write GPS positions
    :param file logger: (Optional) Clean file to write Optimization Error Info

    :return: xyzrgb_array_transformed - georeferenced coordinates
    :rtype: np.array

    :return: parameters
    :rtype: list  [omega, phi, kappa, s, Tx, Ty, Tz]

    :raises IndexError: if such and such

    | **Notes**
    | here

    | **Example**
    | here

    """
    ## Input Data Conversion
    out_tuple = io.load_out(out_file)  # Load OUT File

    #  Load GPS File
    gps_array = np.loadtxt(gps_file, delimiter=' ')

    #  Solve Helmert
    initial_guess = [1, 1, 1, 1, 1, 1, 1]
    solution = _solve_helmert(
        initial_guess, gps_array, out_tuple.cam_array_fixed[:, 0:3], logger=logger)

    # Error Analysis
    if logger:
        _error_analysis_telem(
            solution.parameters, gps_array, out_tuple.cam_array_fixed, solution.gps_array_spline, solution.cam_array_spline, logger)

    #  Apply Helmert to Coordinates of Points
    transformed_array = apply_helmert(
        solution.parameters, out_tuple.xyzrgb_array[:, 0:3])

    #  Recombine coordinates and colors
    xyzrgb_array_transformed = np.hstack(
        (transformed_array, out_tuple.xyzrgb_array[:, 3:]))

    return xyzrgb_array_transformed, solution.parameters


def _solve_helmert(initial_guess, gps_array, cam_array, logger=None):
    """
    Finds the best fit parameters for a Helmert transformation

    :param list initial_guess: seven float values for optimization algorithm
                                    to start
    :param np.array gps_array: 3D array of gps positions from LOG file
    :param np.array cam_array: 3D array of cameras from OUT file

    :return: solution
    :rtype: tuple

    | Solution Tuple Contents:
    |   solution.parameters         (Unknown format) <list>
    |                                   [omega, phi, kappa, s, Tx, Ty, Tz]
    |   solution.gps_array_spline   <numpy array>
    |   solution.cam_array_spline   <numpy array>

    :raises IndexError: if such and such

    | **Notes**
    | here

    | **Example**
    | here

    """
    start = time.time()

    GPSlength = float(gps_array.shape[0])
    CAMlength = float(cam_array.shape[0])
    GPSIdx = np.arange(GPSlength)
    CAMIdx = np.arange(CAMlength)
    lengthScale = CAMlength/GPSlength
    GPSIdxScale = np.array(GPSIdx*lengthScale, dtype=int)
    scaledCAMlist = cam_array[GPSIdxScale]

    ## Compute splines
    #define GPS columns
    GPSx = gps_array[:, 0]
    GPSy = gps_array[:, 1]
    GPSz = gps_array[:, 2]

    #define cam columns
    CAMx = cam_array[:, 0]
    CAMy = cam_array[:, 1]
    CAMz = cam_array[:, 2]

    # Find and print doubles to log file (computeSplines)
    #mask = ((diff(GPSx) == 0) & (diff(GPSy) == 0) & (diff(GPSz) == 0))
    #mask = ((diff(CAMx) == 0) & (diff(CAMy) == 0) & (diff(CAMz) == 0))

    # splprep - find B-spline
    # splev - evaluate B-spline
    #define splprep spline parameters
    s = 3.0  # smoothness parameter
    k = 2  # spline order
    nest = -1  # estimate of number of knots needed (-1 = maximal)

    #find knot points and eval pline with interpolated points for GPS
    tckp, u = sp_interpolate.splprep([GPSx, GPSy, GPSz], s=s, k=k, nest=nest)
    Gxnew, Gynew, Gznew = sp_interpolate.splev(np.linspace(0, 1, 100), tckp)

    #find knot points and eval pline with interpolated points for CAM
    tckp, u = sp_interpolate.splprep([CAMx, CAMy, CAMz], s=s, k=k, nest=nest)
    Cxnew, Cynew, Cznew = sp_interpolate.splev(np.linspace(0, 1, 100), tckp)

    #generate the output array
    splinePoints_array = np.column_stack(
        (Cxnew, Cynew, Cznew, Gxnew, Gynew, Gznew))

    CAM_splineArray = splinePoints_array[:, 0:3]
    GPS_splineArray = splinePoints_array[:, 3:6]

    ## Optimize
    # find optimal_params for local minimum
    unknowns = sp_optimize.fmin_powell(
        _resid, initial_guess, args=(CAM_splineArray, GPS_splineArray))

    parameters = []
    [parameters.append(float(i)) for i in unknowns]

    sol = collections.namedtuple(
        'Solution', ['parameters', 'gps_array_spline', 'cam_array_spline'])

    solution = sol(parameters, GPS_splineArray, CAM_splineArray)

    print "   _solve_helmert time:", time.time()-start
    return solution


def _resid(p, raw, exp):
    """
    Computes the error and returns a sum of squared errors number
    given the 7-parameters, the untransformed coords and the expected coords

    :param list p: seven parameters
                        [omega, phi, kappa, s, Tx, Ty, Tz]
    :param np.array raw: untransformed coordinates (Cameras)
    :param np.array exp: expected coordinates (GPS coordinates)

    :return: sumSquareError
    :rtype: float

    :raises IndexError: if such and such

    | **Notes**
    | here

    | **Example**
    | here

    """
    # Apply helmert tranform
    transformed_array = apply_helmert(p, raw)
    Xp = transformed_array[:, 0]
    Yp = transformed_array[:, 1]
    Zp = transformed_array[:, 2]

    # find the error between the expected and approximated values.
    errX = exp[:, 0] - Xp
    errY = exp[:, 1] - Yp
    errZ = exp[:, 2] - Zp

    i = 0
    err_vector = []
    while i < (len(raw)):
    # starts with a blank array, then adds to it the X,Y,Z errors in that order
    # essentially appending the error calcs for one point pair onto a vector
        err_vector = err_vector + [errX[i], errY[i], errZ[i]]
        i = i+1

    sumSquareError = 0
    for elem in err_vector:
        squareElem = elem * elem
        sumSquareError += squareElem

    return sumSquareError


def _error_analysis_telem(parameters, gps_array, cam_array, gps_array_spline, cam_array_spline, logger):
    """
    Provides error analysis of fit between GPS and Cameras

    :param array parameters: optimized parameters for helmert transform
    :param np.array gps_array: array of gps positions from LOG file
    :param np.array cam_array: array of cameras from OUT file
    :param np.array gps_array_spline: interpolated gps_array (expected)
    :param np.array cam_array_spline: interpolated cam_array (raw)
    :param file logger: (Optional) file to write Optimization Error Info

    :raises IndexError: if such and such

    | **Notes**
    | here

    | **Example**
    | here

    """
    start = time.time()
    raw = cam_array_spline
    exp = gps_array_spline

    # SETUP LOGGER
    logger.write("\nError Analysis Helmert\n")
    logger.write("   Parameters: omega, phi, kappa, s, Tx, Ty, Tz\n")
    logger.write("   Parameters: ")
    for par in parameters:
        logger.write("%s " % par)
    logger.write("\n")

    ## ModelFitError on CAM_spline_array,  GPS_spline_array
    # resid (uses apply_helmert results to compute error (XYZ?))
    residualErrorVal = _resid(parameters, raw, exp)
    logger.write("   Residual Error (SumSquaredError): %f\n" % residualErrorVal)

    # Run the Helmert
    transformed_array = apply_helmert(parameters, raw)
    Xp = transformed_array[:, 0]
    Yp = transformed_array[:, 1]
    Zp = transformed_array[:, 2]

    # find the error between the expected and approximated values.
    # calculates all values at one time
    # WRITE TO LOGGER?
    errX = exp[:, 0] - Xp
    errY = exp[:, 1] - Yp
    errZ = exp[:, 2] - Zp

    """
    # Individual coordinate stats
    # If necessary, write to logger
    for i in range(len(errX)):
        _error_coordinate(raw[i], exp[i], errX[i], errY[i], errZ[i], logger)
    """
    sumSqXYError = 0
    sumSqZError = 0

    for elem in errX:
        xSquare = elem * elem   # x_1^2 + x_2^2 + ... +x_n^2
        sumSqXYError += xSquare

    for elem in errY:
        ySquare = elem * elem
        sumSqXYError += ySquare

    for elem in errZ:
        zSquare = elem * elem
        sumSqZError += zSquare

    # RMSE
    model_xy_rmse = np.sqrt((sumSqXYError / (raw.shape[0])))
    model_z_rmse = np.sqrt((sumSqZError / (raw.shape[0])))
    model_resid_rmse = np.sqrt((residualErrorVal / (raw.shape[0])))

    """
    # Success Metric Level 1 (Part A)
        - georeferencing precision < 5 meters XY RMSE
                < 3 meters Z RMSE
    """
    if logger:
        if((model_xy_rmse < 5) and (model_z_rmse < 3)):
            logger.write("\nEcosynther Quality Test Level 1 (Part A): Success\n")
        else:
            logger.write("\nEcosynther Quality Test Level 1 (Part A): Failure\n")
        logger.write("   Model XY RMSE: %f\n" % model_xy_rmse)
        logger.write("   Model Z RMSE: %f\n" % model_z_rmse)
        logger.write("   Model Residual RMSE: %f\n" % model_resid_rmse)

    # GPS Path Error on CAM_array, GPS_array
    CAM = apply_helmert(parameters, cam_array)
    GPS = gps_array

    CAMDistances = np.empty([CAM.shape[0], 7], dtype=float)

    pointCounter = 0
    for camera in CAM:
        dist2GPSidx = np.argsort(np.sqrt(np.sum((GPS - camera)**2, axis=1)))
        closest2 = dist2GPSidx[:2]
        X0 = camera
        X1 = GPS[closest2[0]]
        X2 = GPS[closest2[1]]

        XYZDistance = _calc3DDistance(X0, X1, X2)
        XYDistance, ZDistance = _calc2DDistance(X0, X1, X2)
        XYZDistanceCheck = np.sqrt(XYDistance**2 + ZDistance**2)

        CAMDistances[pointCounter] = camera[0], camera[1], camera[2],XYDistance, ZDistance, XYZDistance, XYZDistanceCheck 
        pointCounter += 1

    # Write stats to Logger - especially RMSE
    logger.write("\nNote: camera distance vector stats not yet integrated\n")
    # Find out what columns mean
    """
    _vector_stats(CAMDistances[:, 5], logger)
    _vector_stats(CAMDistances[:, 3], logger)
    _vector_stats(CAMDistances[:, 4], logger)
    """
    print "   _error_analysis_telem time:", time.time()-start
    return


def _vector_stats(vector, logger=None):
    """
    (NOTE: Unused)
    """
    if logger:
        RMSE = np.sqrt(sum(vector**2) / vector.shape[0])
        vectorMean = np.mean(vector)
        vectorMAE = np.mean(abs(vector))
        vectorMedian = sp_stats.scoreatpercentile(vector, 50)
        vectorSTD = np.std(vector)
        vectorCV = vectorSTD / vectorMean
        vectorRange = np.min(vector), np.max(vector)
        vector95 = sp_stats.scoreatpercentile(vector, 95)

        # Write to Logger
        # RMSE, vectorMean, vectorMAE, vectorMedian, vectorSTD, vectorCV, vectorRange, vector95

    return


def _calc3DDistance(X0, X1, X2):
    """
    Calculates the XYZ distance
    """

    XYZNum = np.sqrt(np.sum((np.cross((X0-X1), (X0-X2)))**2))
    XYZDen = np.sqrt(np.sum((X2-X1)**2))
    XYZDistance = XYZNum / XYZDen
    return XYZDistance


def _calc2DDistance(X0, X1, X2):
    """
    Calculates the XY and Z distances
    """

    #temp save the Z values
    X0t = X0[2]
    X1t = X1[2]
    X2t = X2[2]
    ZDistance = X0[2] - (X1[2]+X2[2])/2.

    #remake the Z values as 0
    X0[2] = 0
    X1[2] = 0
    X2[2] = 0
    XYDistance = _calc3DDistance(X0, X1, X2)

    #reset the Z values to original
    X0[2] = X0t
    X1[2] = X1t
    X2[2] = X2t
    return XYDistance, ZDistance


def _error_coordinate(raw, exp, errX, errY, errZ, logger):
    """
    (NOTE: Unused)
    Calculates individual coordinate errors and writes output to logger
    """
    xyError = np.sqrt(errX * errX + errY * errY)
    zError = np.sqrt(errZ * errZ)
    xyzError = np.sqrt(errX * errX + errY * errY + errZ * errZ)

    rawCoord = raw[i]
    expCoord = exp[i]
    rawX = rawCoord[0]
    rawY = rawCoord[1]
    rawZ = rawCoord[2]
    expX = expCoord[0]
    expY = expCoord[1]
    expZ = expCoord[2]

    coords = " %.6f" % rawX
    coords += " %.6f" % rawY
    coords += " %.6f" % rawZ
    coords += " %.3f" % expX
    coords += " %.3f" % expY
    coords += " %.3f" % expZ
    coords += " %.3f" % Xp[i]
    coords += " %.3f" % Yp[i]
    coords += " %.3f" % Zp[i]

    errors = "%.3f" % xyError
    errors += " %.3f" % zError
    errors += " %.3f" % xyzError


def apply_helmert(parameters, raw):
    """
    (NOTE: Check to make sure output array has correct shape)
    Applies Helmert transform to a coordinate array given a seven
    parameter array

    :param list parameters: optimized parameters for helmert transform
    :param np.array raw: coordinate array to be transformed

    :return: transformed_array (x y z)
    :rtype: np.array

    | **Notes**
    | here

    | **Example**
    | here

    """
    omega, phi, kappa, s, Tx, Ty, Tz = parameters

    # Rotation equations
    m11 = np.cos(phi) * np.cos(kappa)
    m12 = np.sin(omega) * np.sin(phi) * np.cos(kappa) + np.cos(omega) * np.sin(kappa)
    m13 = (-1) * np.cos(omega) * np.sin(phi) * np.cos(kappa) + np.sin(omega) * np.sin(kappa)
    m21 = (-1) * np.cos(phi) * np.sin(kappa)
    m22 = (-1) * np.sin(omega) * np.sin(phi) * np.sin(kappa) + np.cos(omega) * np.cos(kappa)
    m23 = np.cos(omega) * np.sin(phi) * np.sin(kappa) + np.sin(omega) * np.cos(kappa)
    m31 = np.sin(phi)
    m32 = (-1) * np.sin(omega) * np.cos(phi)
    m33 = np.cos(omega) * np.cos(phi)

    # Transform coordinates
    Xp = (s)*(m11*raw[:, 0]+m21*raw[:, 1]+m31*raw[:, 2])+Tx
    Yp = (s)*(m12*raw[:, 0]+m22*raw[:, 1]+m32*raw[:, 2])+Ty
    Zp = abs(s)*(m13*raw[:, 0]+m23*raw[:, 1]+m33*raw[:, 2])+Tz

    transformed_array = np.vstack((Xp, Yp, Zp)).transpose()
    return transformed_array


def apply_helmert_wo_Tx_Ty(params, raw):
    """
    Performs transformation without X and Y translation

    :return: transformed_array (x y z)
    :rtype: np.array
    """

    omega, phi, kappa, s, Tx, Ty, Tz = params

    # Rotation equations
    m11 = np.cos(phi) * np.cos(kappa)
    m12 = np.sin(omega) * np.sin(phi) * np.cos(kappa) + np.cos(omega) * np.sin(kappa)
    m13 = (-1) * np.cos(omega) * np.sin(phi) * np.cos(kappa) + np.sin(omega) * np.sin(kappa)
    m21 = (-1) * np.cos(phi) * np.sin(kappa)
    m22 = (-1) * np.sin(omega) * np.sin(phi) * np.sin(kappa) + np.cos(omega) * np.cos(kappa)
    m23 = np.cos(omega) * np.sin(phi) * np.sin(kappa) + np.sin(omega) * np.cos(kappa)
    m31 = np.sin(phi)
    m32 = (-1) * np.sin(omega) * np.cos(phi)
    m33 = np.cos(omega) * np.cos(phi)

    # Transform coordinates
    Xp = (s)*(m11*raw[:, 0]+m21*raw[:, 1]+m31*raw[:, 2])
    Yp = (s)*(m12*raw[:, 0]+m22*raw[:, 1]+m32*raw[:, 2])
    Zp = abs(s)*(m13*raw[:, 0]+m23*raw[:, 1]+m33*raw[:, 2]) + Tz

    transformed_array = np.vstack((Xp, Yp, Zp)).transpose()
    return transformed_array


def georef_grnd_cntrl():
    """
    (NOTE: Unimplemented)

    This is a one-sentence summary

    :param str a: A string to be converted
    :param integ v: A string to be converted
    :param type b: optional parameter

    :return: the return
    :rtype: int

    :raises IndexError: if such and such

    | **Notes**
    | here

    | **Example**
    | here

    """

    pass
