#!/bin/python

# Copyright (c) 2013, Regents of the University of California
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import print_function

import sys
import os
import argparse
import vcf

# trying to avoid using our classes for reasons of speed

def record_to_str(record):
    return "%s %d %s %s" % (record.CHROM, record.POS,record.REF,record.ALT)

def record_reverse(r1,r2):
    return r1.REF == r2.ALT[0] and r2.REF == r1.ALT[0]

def parse_args(params):
    def is_valid_file(parser, arg):
        if not os.path.exists(arg):
            parser.error('The file {} does not exist!'.format(arg))
        else:
            return arg
    parser = argparse.ArgumentParser(description="""
        Check VCF for violating assumptions SMaSH makes.
        Assume that input VCF is sorted by position.
    """)
    parser.add_argument('vcf_to_check', type=lambda v: is_valid_file(parser, v))
    args = parser.parse_args(params)
    return args

def check_for_same_locations(vcf_file):
    pass

def check_for_overlaps(vcf_file):
    pass

def build_record_dict(check_vcf,record_dict={}):
    for r in check_vcf:
        if r.CHROM not in record_dict:
            record_dict[r.CHROM] = {}
            record_dict[r.CHROM][r.POS] = r
        else:
            if r.POS in record_dict[r.CHROM]:
            #print("There is already a variant on at location " + str(r.POS) + ": " + record_to_str(r) + ", " + record_to_str(record_dict[r.POS]))
                if record_reverse(r,record_dict[r.CHROM][r.POS]):
                    print("reversed variants " + record_to_str(r) + " " + record_to_str(record_dict[r.CHROM][r.POS]))
                else:
                    print(record_to_str(r) + " " + record_to_str(record_dict[r.CHROM][r.POS]))
            else:
                record_dict[r.CHROM][r.POS] = r
    return record_dict

def main(params):
    args = parse_args(params)
    with open(args.vcf_to_check) as f:
        check_vcf = vcf.Reader(f)
        record_dict = build_record_dict(check_vcf)
    print("Done!")


if __name__ == "__main__":
    main(params=sys.argv[1:])
