#!C:\Python27\python.exe
# encoding: utf-8
'''
Created on 3 Aug 2014

@author: Liam Deacon

@contact: liam.deacon@diamond.ac.uk

@copyright: 2014 Liam Deacon

@license: MIT License

'''

import pickle
                    
import pprint
import os.path, time, glob, sys
from igor.record.wave import WaveRecord
from igor.script import Script

import numpy
from numpy import *

import igor.packed as ipx 
import igor.binarywave as ibw
from igor.record.wave import WaveRecord
from igor.script import Script

numpy.set_printoptions(threshold=numpy.nan)

def wave_header(wave):
    comment = ""

    try:
        exponents = "dimExponents=" + ", ".join(["".join(unit) for unit 
                        in wave['wave']['wave_header']['dimEUnits']]) + "\n"
    except:
        exponents = ""
    
    try:
        units = "dimUnits=" + ", ".join(["".join(unit) for unit 
                        in wave['wave']['wave_header']['dimUnits']]) + "\n"
    except:
        units = ""
         
    notes = "\n".join([note for note in wave['wave']['note']])
    notes = notes.replace('\n', "").replace('\r', '\n')
    
    for key in wave['wave']['wave_header']:
        if key in ['sfA', 'sfB', 'bname', 'npnts']:
            comment += "%s=%s\n" %(key, str(
                    wave['wave']['wave_header'][key]).replace('\n', ''))
            
    header = str(file) + str(notes) + str(exponents) + str(units) + str(comment)
    
    return header


class PackedScript (Script):
    def _run(self, args):
        self.args = args
        
        if os.path.isdir(args.infile):
            files = glob.glob(os.path.join(os.path.abspath(
                                                    args.infile), '*.pxt'))
            files += glob.glob(os.path.join(os.path.abspath(
                                                    args.infile), '*.pxp'))
            
            basenames = [os.path.splitext(base)[0] for base in files]
            for ibw in glob.glob(os.path.join(
                                    os.path.abspath(args.infile), '*.ibw')):
                basename = os.path.splitext(ibw)[0]
                if basename not in basenames:
                    files.append(ibw)
            
        elif os.path.isfile(args.infile):
            files = [args.infile]
        else:
            raise ValueError("Invalid input path specified!")
        
        for infile in files:
            infile = os.path.abspath(infile)

            filestr = str("PYTHON -> Converted from IGOR experiment file '%s'\n" 
                          % os.path.basename(infile))
            modified = "Modified=%s\n" % time.ctime(os.path.getmtime(infile))
            created = "Created=%s\n" % time.ctime(os.path.getctime(infile))
            
            if isinstance(args.outfile, file):
                outfile, ext = os.path.splitext(infile)
                path = os.path.dirname(infile)
                outfile_basename = os.path.join(path, infile)   
            elif os.path.isdir(os.path.dirname(args.outfile)):
                ext = '.txt'
                path = os.path(args.outfile)
                outfile_basename = os.path.join(path, args.outfile)   
            else:
                outfile, ext = os.path.splitext(infile)
                path = os.path.dirname(args.outfile)
                outfile_basename = os.path.join(path, args.outfile)   
            
            outfile = os.path.splitext(os.path.basename(infile))[0]     

            if os.path.splitext(infile)[1] == '.ibw':
                records = [ibw.load(infile)]
            elif os.path.splitext(infile)[1] in ['.pxt', '.pxp']:
                records, filesystem = ipx.load(infile)
            
            for i, wave in enumerate(records):
                try:
                    
                    #wave = pickle.dumps(wave)
                    #wave = pickle.loads(wave)
                    wave = eval(str(wave))
                    
                    notes = filestr + wave_header(wave) + created + modified
    
                    if len(records) > 1:
                        outfile = str(outfile_basename) + '_{}'.format(i)
        
                    outfile += '.txt'
        
                    numpy.savetxt(outfile, wave['wave'].get('wData'), 
                                  fmt='%g', delimiter='\t', header=notes)
                    print("Successfully converted '%s' -> '%s'" % (infile, outfile))
                except AttributeError:
                    sys.stderr.write("Error: Unable to convert '%s' to ASCII\n"
                                      % infile)

                    
if __name__ == "__main__":
    s = PackedScript(
        description=__doc__, filetype='IGOR Packed Experiment (.pxp) file')
    s.run()