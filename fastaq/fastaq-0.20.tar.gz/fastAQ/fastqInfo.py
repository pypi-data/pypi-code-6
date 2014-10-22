# -*- coding: utf-8 -*-
#	Parsing a fastq file.
#	Author - Janu Verma
#	jv367@cornell.edu

import sys
from trimming import Trimming
from sequenceOperations import SequenceManipulation

class FastqParser:
	"""
	Parses a FASTQ file to extract the sequences and the base qualities. 

	Parameters
	----------
	fasta_file : Fastq file to be parsed. 


	Example
	-------
	>>> import sys
	>>> input_file = sys.argv[1] 
	>>> out = FastqParser(input_file)
	>>> seqDict = out.sequenceDict()
	>>> print len(seqDict.keys())
	"""

	def __init__(self, fastq_file):
		self.ff = fastq_file
		
	def readFastq(self, fastqFile):
		"""
		Reads and parser the FASTQ file. 

		Parameters
		----------
		fastqFile - A FASTQ file.

		Returns
		------
		Generator object containing sequences. 
		"""
		i = 1
		name, seq, baseQ = None, [], []
		for line in fastqFile:
			if (line.startswith("@")) and (i%4 != 0):
				if name: yield (name, ''.join(seq), ''.join(baseQ))
				name, seq, baseQ = line, [], []
			if (line[0] in ['A', 'G', 'T', 'C', 'N']):
				seq.append(line)
			if (i%4 == 0):
				baseQ.append(line)
			i += 1
		if name: yield (name, ''.join(seq), ''.join(baseQ))	




	def sequenceDict(self):
		"""
		Creates a dictionary of sequences with their header.

		Returns
		-------
		A dictionary of sequences.
		"""
		with open(self.ff) as fastaFile:
			sequences = {}
			for name,seq,baseQ in self.readFastq(fastaFile):
				sequences[name.strip()] = seq.strip()
			return sequences
	



	def baseQualities(self):
		"""
		Creates a dictionary of base qualities of the sequences.

		Returns
		-------
		A dictionary of base qualities.
		"""
		with open(self.ff) as fastaFile:
			qualities = {}
			for name,seq,baseQ in self.readFastq(fastaFile):
				qualities[name.strip()] = baseQ.strip()
			return qualities



	def seqNames(self):
		"""
		Names/Headers of all the sequences.

		Returns
		-------
		A list of names of all the sequences in the FASTQ file. 
		"""
		seqDict = self.sequenceDict()
		return seqDict.keys()


	def trimSeq(self, name, qualityCutOff=0, byInterval=False, interval=None, mott=False, limitValue=None):
		"""
		Trims the sequence.

		Parameters
		----------
		name : Name/header of the sequence to be trimmed.
		qualityCutOff : Threshold value of the quality for trimming sequence based on removing low quality bases.
		byInterval : If True, the sequence will be trimmed by removing bases according to the given interval.
		interval : The interval containing the number of bp's to be trimmed from left and right side respectively.
					Need byInterval to be True.
		mott : If True, the sequence will be trimmed according to the Mott's algorithm.
		limitValue : Numerical value of the limit to be used in Mott's algorithm. 
					Requires mott to be True.			 
		
		Returns
		-------
		Trimmed sequence.			
		"""
		seqDict = self.sequenceDict()
		qualDict = self.baseQualities()
		sequence = seqDict[name]
		quality = qualDict[name]
		trimmer = Trimming(sequence, quality)
		if (byInterval):
			return trimmer.trimSequence(interval)
		elif (mott):
			return trimmer.mott(limitValue)
		else:
			return trimmer.lowQualTrim(qualityCutOff)	


	def maskSeq(self, name, interval, toLower=False, maskingChar='N'):
		"""
		Masks the sequence based on the given interval. 

		Parameters
		---------
		name: Name/header of the sequence.  
		interval: A tuple containing the start and end positions for the masking. 
		toLower: If True, the sequence in the interval is converted to lower case bases.
						Default is False. 
		maskingChar :  Masking character. Default is 'N'.

		Returns
		-------
		Masked sequence.
		"""
		seqDict = self.sequenceDict()
		sequence = seqDict[name]
		masker = SequenceManipulation(sequence)
		return masker.maskSequence(interval, toLower=False, maskingChar='N')

					

	def maskAll(self, intervals, toLower=False, maskingChar='N'):
		"""
		Masks the sequences in the FASTA file based on the given intervals. 

		Parameters
		--------- 
		intervals: A list of tuples containing the start and end positions for the masking. 
		toLower: If True, the sequence in the interval is converted to lower case bases.
						Default is False. 
		maskingChar :  Masking character. Default is 'N'.

		Returns
		-------
		Masked sequences.
		"""
		seqDict = self.sequenceDict()
		for i in range(len(seqDict.keys())):
			x = seqDict.keys()[i]
			interval = intervals[i]
			print self.maskSeq(x, interval, toLower=False, maskingChar='N')
	



	def trimAll(self, qualityCutOff=0, byInterval=False, intervals=None, mott=False, limitValue=None):
		"""
		Trims all the sequence in the FASTA file from both sides based on the intervals.

		Parameters
		----------
		interval : A list of tuples containing the number of bp's to be trimmed from left and right side respectively.

		Returns
		-------
		Trimmed sequences.			
		"""
		seqDict = self.sequenceDict()
		for i in range(len(seqDict.keys())):
			x = seqDict.keys()[i]
			interval = intervals[i]
			print self.trimSeq(x, qualityCutOff=0, byInterval=False, interval=None, mott=False, limitValue=None)


	def reverseComplement(self, nameSeq):
		"""
		Compute the reverse complement of a given sequence. 

		Parameters
		----------
		sequence: Name of the sequence whose reverse complement is to be computed. 

		Returns
		-------
		sequence which is the reverse complement of the input sequence.
		"""
		seqDict = self.sequenceDict()
		sequence = seqDict[nameSeq]
		new_seq = SequenceManipulation(sequence)
		return new_seq.reverseComplement()



	def reverseComplementAll(self):
		"""
		Compute the reverse complements of all the sequences in the given FASTA file. 

		Parameters
		----------
		sequence: Name of the sequence whose reverse complement is to be computed. 

		Returns
		-------
		Prints the reverse complements.
		"""
		seqDict = self.sequenceDict()
		for i in range(len(seqDict.keys())):
			x = seqDict.keys()[i]
			print self.reverseComplement(x)	







			

















