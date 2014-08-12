# -*- coding: utf-8 -*-
# -*- python -*-
#
#  This file is part of the easydev package
#
#  Copyright (c) 2012-2014 
#
#  File author(s): Thomas Cokelaer (cokelaer@gmail.com)
#
#  Distributed under the GLPv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: 
#
##############################################################################
import argparse



# example

class OptionParser(object):
    def  __init__(self, prog, args):
        thisid = "$Id: apps.py 4007 2013-09-13 15:17:32Z cokelaer $"
        usage = """%s 

        bioconvert -i model.sif -o model.net
        bioconvert --help
        bioconvert --input model.sif --midas data.csv --output test.json

        Author: Thomas Cokelaer, cokelaer@ebi.ac.uk
        Version: %s

        """ % (prog, thisid)
        self.parser = argparse.ArgumentParser(usage=usage, version=thisid,
            prog=prog, description=description, add_help=True)
        self.add_general_options()
        self.options = self.parser.parse_args(args)

    def add_general_options(self):
        self.parser.add_argument("--verbose", action="store_true", default=False)
        self.parser.add_argument("--input",  dest="input",default=None)
        self.parser.add_argument("--midas",  dest="midas",default=None)
        self.parser.add_argument("--output", dest="output",default=None)

def bioconvert(args=None):
    """The main application available when installing bioconvert

    Type::

        bioconvert --help 

    For developers:

    :param  options: a options object returned by :mod:`argparse.parser.parse_args`
    :param  config: a config file (ini) as returned by DynamicConfigParser (not
        documented here, but in :mod:`cinapps.greedy.config`

    """
    if args == None:
        import sys
        args = sys.argv[:]
    parser = OptionParser("bioconvert", args[1:])
    options = parser.options

    if options.input == None  or options.output == None:
        print("Both --input and --output must be provided\n\n")
        OptionParser("bioconvert", ["--help"])


    inp = os.path.splitext(options.input.lower())[1]
    inp = inp[1:]
    out = os.path.splitext(options.output.lower())[1]
    out = out[1:]

    if out == "json":
        if options.midas == None:
            raise ValueError("If output is json, you must provide a midas file with the --midas option")


    from bioconvert.registered import check_registered
    check_registered(inp ,out)

    if inp == 'sif' and out == 'net':
        print("Converting SIF file to NET file.")
        from bioconvert import sif2asp
        c = sif2asp.SIF2ASPnet(options.input)
        print("Saving into %s" % options.output)
        c.write2net(options.output)
    elif inp == 'net' and out == 'sif':
        print("Converting NET file to SIF file")
        from bioconvert import asp2sif
        c = asp2sif.ASPnet2SIF(options.input)
        print("Saving into %s" % options.output)
        c.write2sif(options.output)
    elif inp == 'csv' and out == 'obs':
        print("Converting MIDAS file to OBS file")
        from bioconvert import midas2asp
        c = midas2asp.MIDAS2ASPobs(options.input)
        c.convert()
        print("Saving into %s" % options.output)
        c.write2obs(options.output)
    elif inp == 'sif' and out == 'json':
        print("Converting SIF file to NET file.")
        from bioconvert import sif2json
        c = sif2json.SIF2JSON(options.input, options.midas)
        c.convert()
        print("Saving into %s" % options.output)
        c.write2json(options.output)