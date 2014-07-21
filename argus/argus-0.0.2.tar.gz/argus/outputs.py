#!/usr/bin/env python
"""
Output stuff for calibration results.  First the raw output is saved
as a csv. The csv is read back in using pandas, in order to threshold
and give summary information. 
"""

import logging
import pandas
import cv2
import numpy as np

def to_csv(results,ofilename,header=True):
    """
    This dumps the raw result of a simplified calibration run to a csv
    file with a header.  The header gives the columns, which are 
    f,cx,cy,AR,s,k1,k2,t1,t2,k3,rmse
    """
    ofile = file(ofilename,"w")
    results.sort(key=lambda cam: cam.rmse)
    if header:
        ofile.write("f,cx,cy,AR,s,k1,k2,t1,t2,k3,rmse\n")
    for R in results:
        ofile.write(str(R)+"\n")
    ofile.close()
    logging.info("results written to {0}".format(ofilename))






def summarize(ofilename,threshold=1.1,mthreshold=0.1):
    """
    Provides an on-screen summary of the calibration results by printing
    the best 5, printing the ranges for within threshold(default 1.1) of
    the best rmse, and printing the best result (lowest rmse). 
    """
    data = pandas.read_csv(ofilename)
    print("summary for calibration file {0}".format(ofilename))
    print(data.head())
    print("{0} calibrations obtained".format(len(data)))

    good = data[data.rmse < threshold*data.rmse.iloc[0]]
    print("{0} calibrations are within {1} of best\n".format(len(good),threshold))
    
    best = data.iloc[0]
    low = good.min()
    high = good.max()
    print("rmse range:      {0} < {1} < {2}\n".format(low.rmse,best.rmse,high.rmse))
    print("ranges for each calibration parameter")
    print("focal length f:  {0} < {1} < {2}".format(low.f,best.f,high.f))
    print("principal pt cx: {0} < {1} < {2}".format(low.cx,best.cx,high.cx))
    print("principal pt cy: {0} < {1} < {2}".format(low.cy,best.cy,high.cy))
    print("aspect ratio AR: {0} < {1} < {2}".format(low.AR,best.AR,high.AR))
    print("skew s:          {0} < {1} < {2}".format(low.s,best.s,high.s))
    print("radial k1:       {0} < {1} < {2}".format(low.k1,best.k1,high.k1))
    print("radial k2:       {0} < {1} < {2}".format(low.k2,best.k2,high.k2))
    print("tangential t1:   {0} < {1} < {2}".format(low.t1,best.t1,high.t1))
    print("tangential t2:   {0} < {1} < {2}".format(low.t2,best.t2,high.t2))
    print("radial k3:       {0} < {1} < {2}".format(low.k3,best.k3,high.k3))
    print("\n")

    Nmw = int(np.round(mthreshold*len(data)))
    medianworthy = data.iloc[0:Nmw]
    meed = medianworthy.median() 
    q25 = medianworthy.quantile(0.25)
    q75 = medianworthy.quantile(0.75)
    print("rmse:            {0} < {1} < {2} \n".format(q25.rmse,meed.rmse,q75.rmse))
    print("medians for each calibration parameter in top {0}".format(Nmw))
    print("focal length f:  {0} < {1} < {2}".format(q25.f,meed.f,q75.f))
    print("principal pt cx: {0} < {1} < {2}".format(q25.cx,meed.cx,q75.cx))
    print("principal pt cy: {0} < {1} < {2}".format(q25.cy,meed.cy,q75.cy))
    print("aspect ratio AR: {0} < {1} < {2}".format(q25.AR,meed.AR,q75.AR))
    print("skew s:          {0} < {1} < {2}".format(q25.s,meed.s,q75.s))
    print("radial k1:       {0} < {1} < {2}".format(q25.k1,meed.k1,q75.k1))
    print("radial k2:       {0} < {1} < {2}".format(q25.k2,meed.k2,q75.k2))
    print("tangential t1:   {0} < {1} < {2}".format(q25.t1,meed.t1,q75.t1))
    print("tangential t2:   {0} < {1} < {2}".format(q25.t2,meed.t2,q75.t2))
    print("radial k3:       {0} < {1} < {2}".format(q25.k3,meed.k3,q75.k3))
    print("\n")
    
    print("best calibration found: (rmse={0})".format(best.rmse))
    print(best)
    







# If you wanted to get field of view and focal length, here is how
# but it requires knowing image size and the pixel spacing on the sensor,
# which is specific to camera model. 

#logging.info("best calibration found: rmse={0}".format(results[0].rmse))
#fovx,fovy,focalLength,principalPoint,aspectRatio = cv2.calibrationMatrixValues(results[0].cM,iS,6.248,4.686)
#logging.info("fovx: {0} deg, fovy: {1} deg, focalLength: {2} mm".format(fovx,fovy,focalLength))

