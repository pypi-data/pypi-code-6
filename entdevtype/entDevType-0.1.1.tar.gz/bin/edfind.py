#!/usr/bin/python

from argparse import ArgumentParser as ap 
from sys import exit
from os import path, access, R_OK

import entropyDeviationType

def printBlock(idx, block):

	print "\t\tBN: {0:^5X}\tC: {1:^7.4f}\tS: {2:^7.4f}\tES: {3:^7.4f}\tER: {4:^7.4f}".format(idx, 
																						block.chi_square, 
																						block.shannon,
																						block.estimate,
																						block.error)

	return


parser = ap(description='Accepted Arguments')
parser.add_argument(	'file', 		 
						help='The input file to scan')
parser.add_argument(	'--blocksize',	'-b',
						help='The size of the blocks to split the input file into; specified in bytes',
						default=8192)
parser.add_argument(	'--blockscore', '-s', 
						help='Whether to print the score of all the blocks or not', 
						action='store_true')
parser.add_argument(	'--wholescore',	'-w', 
						help='Whether to print the whole file score or not', 
						action='store_true')
parser.add_argument(	'--blockdev',	'-d', 
						help='Whether to calculate and print deviations for a given block', 
						action='store_true')
parser.add_argument(	'--blocknumber', '-n',
						help='The block number to calculate deviations for',
						default=None)
parser.add_argument(	'--wholedev',	'-o',
						help='Whether to calculate --blocknumber N\'s deviation against the whole file score',
						action='store_true')
parser.add_argument(	'--xydev',		'-y',
						help='Calculate the deviations of block X from block Y',
						nargs=2)
parser.add_argument(	'--seqdev', 	'-q',
						help='Sequential deviation; Calculate the deviations of all blocks from its neighbor blocks',
						action='store_true')
parser.add_argument(	'--seqxy', 		'-e',
						help="The range of blocks to calculate sequential deviation for",
						nargs=2, default=None)
parser.add_argument(	'--suspect',	'-u',
						help="Attempt to identify suspect blocks",
						action='store_true'),
parser.add_argument(	'--frequency','-f',
						help='Iterate across all blocks printing the frequency of each byte',
						 action='store_true')
parser.add_argument(	'--freqcount', 	'-c',
						help='Specifies the number of characters with the highest frequency to print',
						default=None)
parser.add_argument(	'--freqxy',		'-r',
						help='Print the frequency of --freqcount or all bytes in a range of blocks delimited by X and Y',
						nargs=2, default=None)
parser.add_argument(	'--xor',	'-x',
						help='Whether to attempt to find an embedded PE file encrypted with a one-byte XOR key',
						action='store_true')
parser.add_argument(	'--xorall',	'-a',
						help='When specified, the XOR table search will be performed for all possible PE files and not'
							' just the first one',
						action='store_true')

args = parser.parse_args()

if not args.file:
	print "An input file must be specified\n"
	parser.print_help()
	exit(-1)	

if not path.isfile(args.file):
	print "The file '%s' does not exist" % args.file
	exit(-1)

if not access(args.file, R_OK):
	print "The file '%s' is not readable" % args.file
	exit(-1)

if args.blockdev or args.wholedev:
	if args.blocknumber == None:
		raise RuntimeError("One or more options where specified that requires --blocknumber to be specified")

e = entropyDeviationType.entropyDeviationType(args.blocksize)
e.openFile(args.file)
xor = entropyDeviationType.xorTableSearchType(512)
xor.openFile(args.file)

if args.blocknumber:
	if False == e.isValidBlockNumber(args.blocknumber):
		raise RuntimeError("A --blocknumber that exceeds the number of blocks was specified")

if args.xydev:
	if False == e.isValidBlockRange(args.xydev[0], args.xydev[1]):
		raise RuntimeError("A --xydev with a block number that exceeds the number of blocks was specified")

if None != e:
	print "FILE: {0:s} BLOCK COUNT: {1:d} BLOCK SIZE: {2:d}".format(args.file, e.getBlockCount(), long(args.blocksize))

if args.blockscore == True:
	idx = 0
	allScores = e.getAllScores()
	print "\n\tALL SCORES"
	for s in allScores:
		printBlock(idx, s)
#		print "\t\tBN: {0:^5X}\tC: {1:^7.4f}\tS: {2:^7.4f}\tES: {3:^7.4f}\tER: {4:^7.4f}".format(idx,
#																						s.chi_square, s.shannon,
#																						s.estimate, s.error)
		idx += 1


if args.wholescore == True:
	ws = e.getWholeFileScore()

	print "\n\tWHOLE FILE SCORE"
	print "\t\t\t\tC: {0:^7.4f}\tS: {1:^7.4f}\tES: {2:^7.4f}\tER: {3:^7.4f}".format(
																			ws.chi_square, ws.shannon,
																			ws.estimate, ws.error)

if args.xydev != None:
		bx = long(args.xydev[0], 16)
		by = long(args.xydev[1], 16)

		xy = e.getXYDeviation(bx, by) 

		print "\n\tBLOCK {0:^5X} DEVIATION RELATIVE BLOCK {1:^5X}".format(bx, by)
		print "\t\t\t\tC: {0:^7.4f}\tS: {1:^7.4f}\tES: {2:^7.4f}\tER: {3:^7.4f}".format(xy.chi_square, xy.shannon,
																					xy.estimate, xy.error)
if args.blockdev == True:
	bnum = long(args.blocknumber, 16)
	idx = 0
	print "\n\tBLOCK {0:^5X} DEVIATION RELATIVE ALL BLOCKS".format(bnum)

	for dev in e.getBlockAllDeviation(bnum): 
		if idx == bnum:
			idx += 1

		printBlock(idx, dev)
#		print "\t\tBN: {0:^5X}\tC: {1:^7.4f}\tS: {2:^7.4f}\tES: {3:^7.4f}\tER: {4:^7.4f}".format(idx,
#																						dev.chi_square, dev.shannon,
#																						dev.estimate, dev.error)
		idx += 1

	if args.wholedev == True:
		print "\n\tBLOCK {0:^5X} DEVIATION RELATIVE WHOLE FILE".format(bnum)

		wd = e.getWholeFileDeviation(bnum) 
		print "\t\t\t\tC: {0:^7.4f}\tS: {1:^7.4f}\tES: {2:^7.4f}\tER: {3:^7.4f}".format(wd.chi_square, wd.shannon,
																						wd.estimate, wd.error)	

if args.seqdev == True or args.seqxy != None:
	items = list()

	if args.seqxy != None:
		minv = long(args.seqxy[0], 16)
		maxv = long(args.seqxy[1], 16) 
	else:
		minv = 0
		maxv = e.getBlockCount()-1

	items = e.getSequentialDeviation(minv, maxv)

	print "\n\tSEQUENTIAL DEVIATION FOR BLOCKS [{0:^5X}:{1:^5X}]".format(minv, maxv)

	for item in items:
		fidx = 0
		sidx = 0

		if None == item['prior']:
			fidx = item['index']
			sidx = item['next']
		else:
			fidx = item['prior']
			sidx = item['index']

		dev = item['dev']
		print "\t\tBN [{0:^5X}:{1:^5X}]\tC: {2:^7.4f}\tS: {3:^7.4f}\tES: {4:^7.4f}\tER: {5:^7.4f}".format(fidx, sidx,
																										dev.chi_square, 
																										dev.shannon,
																										dev.estimate,
																										dev.error)
if True == args.suspect:
	suspectIndex = 0
	suspectMaxIndex = 0
	tmp = 0
	suspectBlock = None
	suspectRanges = list()
	avgs = list()
	avg = dict()

	items = e.findHighDeviation(100, 20, 1)

	print "\n\tSUSPECT BLOCK CHECK (NOT RELIABLE; EXAMPLE IMPLEMENTATION)"

	for item in items:
		if None == item['prior']:
			suspectIndex = item['next']
		else:
			suspectIndex = item['index']

		if (0 != suspectIndex):
			if e.isHighAverageChi(suspectIndex-1, 15):

				if not e.isValidBlockNumber(suspectIndex+1):
					print "\n\tWARNING: LAST BLOCK SUSPECT: DEVIATION STATISTICS FOR RANGE POTENTIALLY UNRELIABLE"
					continue

				if not e.priorHighAndNextLowShannon(suspectIndex, 20.0, 1.5):
					continue

				suspectMaxIndex = e.getSequentialLowShannon(suspectIndex+1)

				if abs(suspectMaxIndex - suspectIndex) <= 1:
					continue
		
				tmp = e.getSequentialCloseChi(suspectIndex+1, e.getBlockCount()-1)
	
				if suspectMaxIndex < tmp:
					suspectMaxIndex = tmp

				suspectRanges.append(tuple((suspectIndex, suspectMaxIndex)))

	suspectRanges = e.coalesceSequential(suspectRanges, 2)
	
	for sr in suspectRanges:
		if sr[1]-sr[0] == 1 and sr[0] == 0:
			print "\n\tWARNING: FIRST BLOCK SUSPECT: DEVIATION STATISTICS FOR RANGE POTENTIALLY UNRELIABLE"
 
		elif sr[1]-sr[0] == 1 and sr[1] == e.getBlockCount()-1:	
			print "\n\tWARNING: LAST BLOCK SUSPECT: DEVIATION STATISTICS FOR RANGE POTENTIALLY UNRELIABLE"


		print "\n\tBLOCKS [{0:^5X}:{1:^5X}] SUSPECT".format(sr[0], sr[1])

		for idx in range(sr[0], sr[1]):		
			printBlock(idx, e.getScore(idx))

		
if True == args.frequency or None != args.freqcount or None != args.freqxy:
	dis = list()
	cnt = 256
	x 	= 0
	y	= e.getBlockCount()-1
	
	if None != args.freqcount:
		cnt = long(args.freqcount)

	if None != args.freqxy:
		x = long(args.freqxy[0], 16)
		y = long(args.freqxy[1], 16)


	print "\n\tBYTE FREQUENCY FOR BLOCKS [{0:^5X}:{1:^5X}]".format(x, y)

	for idx in range(x, y):
		line = list()
		plc  = 4
		diff = 0
		dis	 = e.calculateDistribution(idx, idx+1)

		if 4 > cnt and 0 != cnt:
			plc = cnt		

		for dcnt in range(0, cnt+1):
			if dcnt >= 256:
				break 
			if dcnt+1 < 256:
				cntz = float(dis[dcnt].count)
				cnto = float(dis[dcnt+1].count)

				if 0 != cnto:
					diff = (abs(cntz-cnto)/((cntz+cnto)/2))*100.0

	
			if plc == len(line):
				print "\t\tBN: {0:^5X}".format(idx),
				for l in line:
					print "[V: %.2X C:%5X P: %7.2f]" % (l[0], l[1], l[2]),
				
				line = list()
				print ""
			else:
				line.append(tuple((dis[dcnt].value, dis[dcnt].count, diff)))

				
if True == args.xor or True == args.xorall:
	if True == args.xorall:
		print "\n\tXOR TABLE SEARCH ALL"

		try:
			for pe in xor.findAll():
				print "\t\tOFFSET: {0:^5X} ({1:^5X})\tKEY: {2:^2X}".format(pe.offset, pe.offset/args.blocksize, pe.key)

		except UserWarning as e:
			print "\t\t%s" % e

	else:
		print "\n\tXOR TABLE SEARCH FIRST"

		try:
			pe = xor.findFirst()
			
			print "\t\tOFFSET: {0:^5X} ({1:^5X})\tKEY: {2:^2X}".format(pe.offset, long(pe.offset)/long(args.blocksize), pe.key)

		except UserWarning as e:
			print "\t\t%s" % e

