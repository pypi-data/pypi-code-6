#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
=========================================================================
        msproteomicstools -- Mass Spectrometry Proteomics Tools
=========================================================================

Copyright (c) 2013, ETH Zurich
For a full list of authors, refer to the file AUTHORS.

This software is released under a three-clause BSD license:
 * Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
 * Neither the name of any author or any participating institution
   may be used to endorse or promote products derived from this software
   without specific prior written permission.
--------------------------------------------------------------------------
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL ANY OF THE AUTHORS OR THE CONTRIBUTING
INSTITUTIONS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
$Maintainer: Pedro Navarro$
$Authors: Pedro Navarro$
--------------------------------------------------------------------------
"""

import sys,os
import getopt

from msproteomicstoolslib.format.ProteinDB import ProteinDB

def usage() :
	print "pseudoreverseDB.py"
	print ("-" * 18)
	print "Pseudoreverse sequence (peptide C-terminal) of a database."
	print "Usage: "
	print "python pseudoreverseDB.py [options]"
	print ""
	print "Options: "
	print "-i	fastafile	--input	Fastafile to be pseudoreversed."
	print "-t 	tag		--tag	Use this tag for decoy proteins. Default: DECOY_"
	print ""
	

def main(argv) :

	fastaFile = ""
	fastaoutput = ""
	decoytag = "DECOY_"
	
	#Get options
	try:
		opts, args = getopt.getopt(argv, "hi:t:",["help","input","tag"])

	except getopt.GetoptError:
		usage()
		sys.exit(2)

	argsUsed = 0
	for opt,arg in opts:
		if opt in ("-h","--help") :
			usage()
			sys.exit()
		if opt in ("-i","--input") :
			fastaFile = arg
			if not os.path.exists(fastaFile) :
				print "The fasta file does not exist!"
				sys.exit(2)
			fileName, fileExtension = os.path.splitext(fastaFile)
			fastaoutput = fileName + "_andDecoy" + fileExtension
			argsUsed += 2
		if opt in ("-t","--tag") :
			decoytag = arg


			
	if len(fastaFile) == 0 :
		print "You must provide a fasta file! Use the -i option."
		usage()
		sys.exit(2)
		

	#Read fasta file
	protDB = ProteinDB()
	protDB.readFasta(fastaFile)
	
	#Pseudo-reverse the DB
	print "inverting sequences..."
	protDB.pseudoreverseDB(decoytag)
	print "...done"
	
	#Write the files, concatenate the results
	tmpoutput = fastaoutput + ".tmp"
	protDB.writeFastaFile(tmpoutput)
	
	filenames = [fastaFile, tmpoutput]
	with open(fastaoutput, 'w') as outfile:
		for fname in filenames:
			with open(fname) as infile:
				for line in infile:
					outfile.write(line)
			outfile.write('\r\n')
	     
	os.remove(tmpoutput)

if __name__ == '__main__':
	main(sys.argv[1:])



