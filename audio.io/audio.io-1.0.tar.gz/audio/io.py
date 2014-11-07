#!/usr/bin/env python
# coding : utf-8

# Python 2.7 Standard Library
from __future__ import division
import atexit
import sys

# Digital Audio Coding
import audio.bitstream
import audio.wave

# Third-Party Libraries
import numpy as np
import pyaudio

_pyaudio = None

@atexit.register
def exit():
    if _pyaudio is not None:
        _pyaudio.terminate()

def play(data, df=44100, scale=None):
    global _pyaudio
    if _pyaudio is None:
        _pyaudio = pyaudio.PyAudio()

    # write-read round trip to normalize the data
    stream = audio.wave.write(data, df=df, scale=scale)
    data = audio.wave.read(stream, scale=False)
    assert data.dtype == np.int16 and len(np.shape(data)) == 2

    output = _pyaudio.open(format   = pyaudio.paInt16  ,
                           channels = np.shape(data)[0],
                           rate     = int(df)          ,
                           output   = True             )
    flat = np.ravel(data.T.newbyteorder())
    stream = audio.bitstream.BitStream(flat)
    raw = stream.read(bytes, len(stream) // 8)

    output.write(raw)
    output.stop_stream()
    output.close()

