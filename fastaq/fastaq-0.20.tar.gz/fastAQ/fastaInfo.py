# -*- coding: utf-8 -*-
#	Parsing a fasta file.
#	Author - Janu Verma
#	jv367@cornell.edu

import sys
from sequenceOperations import SequenceManipulation
from trimming import Trimming


class FastaParser:
	"""
	Parses a FASTA file to extract the sequences and header information, if any. 

	Parameters
	----------
	fasta_file : Fasta file to be parsed. 


	Example
	-------
	>>> import sys
	>>> input_file = sys.argv[1] 
	>>> out = FastaParser(input_file)
	>>> seqDict = out.sequenceDict()
	>>> print len(seqDict.keys())
	"""

	def __init__(self, fasta_file):
		self.ff = fasta_file
		


	def readFasta(self, fastaFile):
		"""
		Reads and parser the FASTA file. 

		Parameters
		----------
		fastaFile - A FASTA file.

		Returns
		------
		Generator object containing sequences. 
		"""	
		name, seq = None, []
		for line in fastaFile:
			line = line.rstrip()
			if (line.startswith(">")):
				if name: yield (name, ''.join(seq))
				name, seq = line, []
			else:
				seq.append(line)
		if name: yield (name, ''.join(seq))




	def sequenceDict(self):
		"""
		Creates a dictionary of sequences with their header.

		Returns
		-------
		A dictionary of sequences.

		"""
		with open(self.ff) as fastaFile:
			sequences = {}
			for name, seq in self.readFasta(fastaFile):
				sequences[name] = seq
		return sequences



	def seqNames(self):
		"""
		Names/Headers of all the sequences.

		Returns
		-------
		A list of names of all the sequences in the FASTA file. 
		"""
		seqDict = self.sequenceDict()
		return seqDict.keys()



	def seqFromName(self, name):
		"""
		Extract the sequence corresponding to the given name. 

		Parameters
		---------
		name : Name of the sequence to be retrieved. 

		Returns
		-------
		Sequence corresponding to the input name. 
		"""
		seqDict = self.sequenceDict()
		return seqDict[name]



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




	def trimSeq(self, name, interval, quality = None):
		"""
		Trims the sequence from both sides based on the interval.

		Parameters
		----------
		name : Name/header of the sequence to be trimmed.
		interval : The interval containing the number of bp's to be trimmed from left and right side respectively.

		Returns
		-------
		Trimmed sequence.			
		"""
		seqDict = self.sequenceDict()
		sequence = seqDict[name]
		trimmer = Trimming(sequence, quality)
		return trimmer.trimSequence(interval)





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




	def trimAll(self, intervals, quality=None):
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
			print self.trimSeq(x, interval, quality = None)





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

























