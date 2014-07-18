#!/usr/bin/env python
"""
This submodule holds Brandon Jackson's code for obtaining synchronization
between two movies using the audio tracks.  Code contributions also from
Dennis Evangelista. 

The movies should have some clear, loud moderate to high frequency tone
in order to ensure good audio sync using and fft-based cross correlation. 
We have found in practice that generic environmental noise has too much
random phase variation and does not provide enough signal.  Care must 
be taken that any sound sources are either individually repeated for each
camera or are located equidistant to all cameras, to avoid phase 
differences from the positioning of the camera microphones. 
"""

import logging
import numpy as np
import cv2
import audioread
import scipy.signal




def get_audio(movie_filename,channel=0):
    """
    Returns the audio track and necessary information from a movie as
    a tuple with (video_fps, samplerate, duration, signal[:,channel]).  
    Default channel is 0.  
    """

    video = cv2.VideoCapture(movie_filename)
    video_fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
    video = None # garbage collect the movie

    with audioread.audio_open(movie_filename) as f:
        samplerate = f.samplerate
        duration = f.duration
        channels = f.channels
        temp = bytearray()
        for chunk in f: #.read_data()??!?
            temp.extend(chunk)
        signal = np.frombuffer(temp, dtype="<i2").reshape(-1, channels)
        signal = signal[::-1]
        return video_fps, samplerate, duration, signal[:,channel]

    # Mac vs Linux oddity: Brandon version has .read_data() 
    # Dennis version .read_data() leads to error, must reverse the signal
    # to get same answer as Brandon on Mac!  It's a bug with 
    # audioread where audioread calls the GStreamer gst.AudioFile thing? 






    
def find_offset(signal0, signal1):
    """
    Returns None if signals are None, otherwise it returns a tuple
    (offset_frames, maxcorr) for the two signals.  

    If the signal0 is longer than 2 minutes it does 1 minute slices.

    EXPECTED BUG: If signal1 is not longer than 2 minutes, this should
    cause some strange problems with indices out of range. 

    Dennis suggests refactoring this to only deal with the full thing? 
    """
    if (signal0 is None) or (signal1 is None):
        return None
    else:
        # unpack stuff
        video_fps, samplerate0, duration0, sig0 = signal0
        _, samplerate1, _, sig1 = signal1

        minutes = int(duration0/60)
        if minutes >= 2:
            logging.debug("Working with 1 minute segments...")
            off_corr = np.zeros((minutes,2))
            for seg in range(minutes):
                logging.debug("...minute {0}".format(seg))
                # Take 1 minute slice of audio tracks
                A = sig0[seg*60*samplerate0:(seg+1)*60*samplerate0]
                B = sig1[seg*60*samplerate1:(seg+1)*60*samplerate1]

                # Compute cross and auto correlation using FFT convolution
                # with time reversed signal.
                # This could be sped up several times?
                corr = scipy.signal.fftconvolve(A,B[::-1],mode="full")
                corr0 = scipy.signal.fftconvolve(A,A[::-1],mode="valid")
                corr1 = scipy.signal.fftconvolve(B,B[::-1],mode="valid")

                # Find lags and correlation coefficient
                maxcorr_lag = corr.argmax()
                maxcorr = numpy.nanmax(corr)/((corr0**0.5)*(corr1**0.5))
                offset_samples = int(len(corr)/2)-maxcorr_lag
                offset_frames = float(offset_samples)/float(samplerate0) \
                    * float(video_fps)
                off_corr[seg,0] = offset_frames
                off_corr[seg,1] = maxcorr

            # Return the median frame offset and correlation coefficient
            # for all the 1 minute slices. 
            median_frame_offset = np.median(off_corr[:,0])
            median_corr_coeff = np.median(off_corr[:,1])
            return median_frame_offset, median_corr_coeff

        else:
            logging.debug("Less than one minute... working with whole")
            off_corr = np.zeros((1,2))

            # Compute cross and auto correlation using FFT convolution
            # with time reversed signal.
            corr = scipy.signal.fftconvolve(sig0,sig1[::-1],mode="full")
            corr0 = scipy.signal.fftconvolve(sig0,sig0[::-1],mode="valid")
            corr1 = scipy.signal.fftconvolve(sig1,sig1[::-1],mode="valid")
            
            # Find lags and correlation coefficient
            maxcorr_lag = corr.argmax()
            maxcorr = np.nanmax(corr)/((corr0**0.5)*(corr1**0.5))
            offset_samples = int(len(corr)/2)-maxcorr_lag
            offset_frames = float(offset_samples)/float(samplerate0) \
                * float(video_fps)
            off_corr[0,0] = offset_frames
            off_corr[0,1] = maxcorr
            return offset_frames, maxcorr

            
            
        
            

    
