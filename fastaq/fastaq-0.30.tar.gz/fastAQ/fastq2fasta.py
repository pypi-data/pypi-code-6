# -*- coding: utf-8 -*-
#	FASTQ to FASTA
#	Author - Janu Verma
#	jv367@cornell.edu

import sys


input_file = open(sys.argv[1])

	
class Fastq2Fasta:
	"""
	Converts a FASTQ file to a FASTA. 

	Paramaters
	----------
	input_file : A FASTQ file. 
	"""
	def __init__(self, input_file):
		self.fastq = input_file

	def conversion(self):
		"""
		Do the conversion.
		"""

		i = 1
		name, seq, baseQ = None, [], []
		for line in self.fastq:
			if (line.startswith("@")) and (i%4 != 0):
				if name: yield (name, ''.join(seq), ''.join(baseQ))
				name, seq, baseQ = line, [], []
			if (line[0] in ['A', 'G', 'T', 'C', 'N']):
				seq.append(line)
			if (i%4 == 0):
				baseQ.append(line)
			i += 1
		if name: yield (name, ''.join(seq), ''.join(baseQ))

	def fasta(self):
		"""
		Prints the output FASTA file.
		"""
		for name,seq,baseQ in self.conversion():
			print '>'+name[1:], seq.strip()


out = Fastq2Fasta(input_file)
out.fasta()
		

















