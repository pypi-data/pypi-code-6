# -*- coding: utf-8 -*-
#	Trimming a FASTQ file.
#	Author - Janu Verma
#	jv367@cornell.edu

import string

baseQdict = {x:ord(x) for x in string.printable}

class Trimming:
	"""
	Trimming a FASTQ sequence. 

	Parameters
	----------
	sequence : The sequence to be trimmed.
	qualities : Base qualities of the bp's in the sequence. 
	"""
	def __init__(self, sequence, qualities):
		self.seq = sequence
		self.qual = qualities


	def lowQualTrim(self, qualCutOff):
		"""
		Trims a sequence by removing low quality bp's. 

		Parameters
		----------
		qualCutOff : The threshold for the quality. The bases with quality below this threshold
					will be removed.

		Returns
		-------
		Trimmed sequence.			
		"""	
		trimmedSeq = ''
		l = len(self.seq)
		if (l != len(self.qual)):
			print "Number of base pairs is not same as the number of quality values."
			return None
		else:
			for i in range(l):
				qScore = baseQdict[self.qual[i]]
				qScore = qScore - 33
				if (qScore >= qualCutOff):
					trimmedSeq += self.seq[i]
			return trimmedSeq 	


	def mott(self, limitValue):
		"""
		Trims a sequence by using Mott's algorithm.

		Parameters
		----------
		limitValue : limiting value. 

		Returns
		------
		Trimmed sequence.
		"""	
		seq = self.seq
		qual = self.qual

		l = len(seq)
		totalLMP = 0.0
		oldLmp = 0.0
		i = 0
		trimmedSeq = ''
		while (i < l):
			qScore = baseQdict[qual[-i-1]]
			qScore -= 33
			expo = float(qScore)/10
			pError = 10**(-expo)
			lmpValue = limitValue - pError
			oldLmp = totalLMP
			totalLMP += lmpValue
			if (totalLMP <= 0.0):
				totalLMP = 0.0
				i +=1 
			else:
				trimmedSeq = seq[-i-1] + trimmedSeq
			if (oldLmp > totalLMP):
				break 	
			i += 1	
		return trimmedSeq


	def trimSequence(self, interval):
		"""
		Trims the sequence from both sides based on the interval.

		Parameters
		----------
		interval : The interval containing the number of bp's to be trimmed from left and right side respectively.

		Returns
		-------
		Trimmed sequence.			
		"""
		sequence =  self.seq
		start,end = interval
		n = len(sequence)
		return sequence[start: -end]	






				
						

 

			


























