#!/usr/bin/env python

r"""

===================
Run script for WHAM
===================

.. codeauthor:: Christoph Wehmeyer <christoph.wehmeyer@fu-berlin.de>
.. codeauthor:: Antonia Mey <antonia.mey@fu-berlin.de>

"""

from pyfeat import run_wham
from pyfeat import read_files
from argparse import ArgumentParser, FileType

if '__main__' == __name__:

    # GET COMMAND LINE ARGUMENTS!
    parser = ArgumentParser()
    parser.add_argument(
            'file',
            help='pyfeat compatible files for evaluation',
            nargs='*',
            metavar='FILE'
        )
    parser.add_argument(
            "--kT_file",
            help="specify a pyfeat compatible kT_file",
            default=None,
            metavar="FILE"
        )
    parser.add_argument(
            "--wham_file",
            help="specify a pyfeat compatible wham_file",
            default=None,
            metavar="FILE"
        )
    parser.add_argument(
            "--maxlength",
            help="limit the number of trajectory frames",
            type=int,
            default=None,
            metavar='INT'
        )
    parser.add_argument(
            "--stride",
            help="Subsampling stride of trajectory frames",
            type=int,
            default=1,
            metavar='INT'
        )
    parser.add_argument(
            "--skiprows",
            help="Number of initial frames skipped",
            type=int,
            default=0,
            metavar='INT'
        )
    parser.add_argument(
            "--verbose",
            help="request verbose output",
            action='store_true'
        )
    parser.add_argument(
            "--maxiter",
            help="limit the number of fixed point iterations",
            type=int,
            default=100,
            metavar='INT'
        )
    parser.add_argument(
            "--ftol",
            help="limit the requested convergence level",
            type=float,
            default=1.0E-3,
            metavar='FLOAT'
        )
    args = parser.parse_args()

    # IMPORT FILES AND EXTRACT RELEVANT INFORMATION - CREATES A DATA OBJECT
    data = read_files( args.file, kT_file=args.kT_file, wham_file=args.wham_file, maxlength=args.maxlength, skiprows = args.skiprows, stride = args.stride, verbose=args.verbose )

    # RUN WHAM ON DATA OBJECT - RETURNS FREE ENERGY / PROBABILITY ESTIMATES FOR ALL MARKOV STATES
    result = run_wham( data, verbose=args.verbose, maxiter=args.maxiter, ftol=args.ftol )

    # WRITE RESULTS TO STDOUT
    result.print_markov()
