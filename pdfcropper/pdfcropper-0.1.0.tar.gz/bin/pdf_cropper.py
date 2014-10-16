#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import sys
import os.path
import argparse

try:
    import pdfcropper
except ImportError:
    sys.path.insert(0, os.path.abspath('../src'))
    import pdfcropper


# Variables ===================================================================
OUT_SUFFIX = "_cropped.pdf"  #: Default suffix for input filename.


# Functions & objects =========================================================
def _get_output_name(fn):
    """
    Compose name of the default output filename.

    For example:
        _get_output_name("/hello/joe.pdf") -> "joe_OUT_SUFFIX"
        _get_output_name("/hello/joe.pdf") -> "joe_cropped.pdf"

    Args:
        fn (str): Path to the input filename.

    Returns:
        str: Path to the output filename.
    """
    fn = os.path.basename(fn)

    return fn.rsplit(".", 1)[0] + OUT_SUFFIX


# Main program ================================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""PDF cropper. This program can be used to crop and remove
                       pages from PDF files."""
    )
    parser.add_argument(
        "-c",
        "--crop",
        nargs=4,
        type=int,
        metavar="X",
        help="""Crop vector for all or even pages. Vector is in format LEFT
                RIGHT TOP BOTTOM. -c 50 50 10 10 for example."""
    )
    parser.add_argument(
        "-e",
        "--crop-odd",
        nargs=4,
        type=int,
        metavar="X",
        help="""Crop vector for odd pages. Vector is in format LEFT RIGHT TOP
                BOTTOM. -c 50 50 10 10 for example."""
    )
    parser.add_argument(
        "-r",
        "--remove",
        type=int,
        nargs="+",
        default=[],
        metavar="PAGE",
        help="Remove following pages. Page numbers starts from zero."
    )
    parser.add_argument(
        "-o",
        "--output",
        nargs=1,
        help="""Save modified file to given destination. If not set, suffix
                '%s' is used.""" % OUT_SUFFIX
    )
    parser.add_argument(
        "filename",
        help="Input filename."
    )
    args = parser.parse_args()

    if not os.path.exists(args.filename):
        sys.stderr.write("Can't open '%s'!\n" % args.filename)
        sys.exit(1)

    if args.crop_odd and not args.crop:
        sys.stderr.write("You have to specify also even vector!\n")
        sys.exit(1)

    if not any([args.crop, args.crop_odd, args.remove]):
        sys.stderr.write("No action selected!\n")
        sys.exit(1)

    input_pdf = pdfcropper.read_pdf(args.filename)

    out_pdf = None
    if args.remove and not args.crop and not args.crop_odd:  # just remove
        out_pdf = pdfcropper.remove_pages(input_pdf, args.pages)
    elif args.crop and not args.crop_odd:  # remove/crop all pages same style
        out_pdf = pdfcropper.crop_all(
            input_pdf,
            *args.crop,
            remove=args.remove
        )
    else:  # crop even and odd pages by different coordinates
        out_pdf = pdfcropper.crop_differently(
            input_pdf,
            args.crop,
            args.crop_odd,
            args.remove
        )

    # output filename - if specified, get user's input, if not, compose generic
    # name using _get_output_name()
    out_fn = _get_output_name(args.filename)
    if args.output:
        out_fn = args.output

    # save output
    pdfcropper.save_pdf(out_fn, out_pdf)
