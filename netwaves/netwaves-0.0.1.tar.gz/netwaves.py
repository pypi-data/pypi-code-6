#!/usr/bin/env python3
import argparse
import itertools
from io import BytesIO

import alsaaudio, audioop

def sink(columns, rows, wav_pointer, ppm_pointer):
    try:
        pointers = [ppm_pointer, wav_pointer]
        header_str = 'P6\n%d %d\n255\n' % (columns, rows)
        header = header_str.encode('ascii')
        ppm_pointer.write(header)
        count = 0
        for i in itertools.count(0, 1):
            for pointer in pointers:
                raw = (yield)
                if isinstance(raw, int):
                    result = [raw]
                else:
                    result = list(raw)
                pointer.write(bytes(result))
                pointer.flush()
            count += len(result)
    except GeneratorExit:
        l = [127] * (columns * rows * 3 - count)
        for pointer in pointers:
            pointer.write(bytes(l))
            pointer.flush()

def microphone():
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
    inp.setchannels(1)
    inp.setrate(8000)
    inp.setformat(alsaaudio.PCM_FORMAT_S8)
    inp.setperiodsize(160)
    return inp

def pipe(columns, rows, basename):
    try:
        s = sink(columns, rows, open('%s.wav' % basename, 'wb'), open('%s.ppm' % basename, 'wb'))
        next(s)
        mic = microphone()
        while True:
            l, data = mic.read()
            if l:
                s.send(data[1:])
    except KeyboardInterrupt:
        s.close()
        raise

def parser():
    p = argparse.ArgumentParser('Record sound as PPM.')
    p.add_argument('basename',
        help = 'Output will be written to $basename{wav,ppm}.')
    p.add_argument('-c', '--columns', type = int, default = 320,
        help = 'Number of columns in the image')
    p.add_argument('-r', '--rows', type = int, default = 180,
        help = 'Number of rows in the image')
    return p

def main():
    p = parser().parse_args()
    import os
    os.system('sleep 1s && feh -FZ -D 0.1 %s.ppm %s.ppm &' % (p.basename, p.basename))
    pipe(p.columns, p.rows, p.basename)

if __name__ == '__main__':
    main()
