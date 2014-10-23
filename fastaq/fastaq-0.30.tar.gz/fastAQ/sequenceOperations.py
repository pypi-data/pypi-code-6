# -*- coding: utf-8 -*-
#	Manipulating Sequences.
#	Author - Janu Verma
#	jv367@cornell.edu



class SequenceManipulation:
	"""
	Edits/Modifies a DNA sequence.

	Parameters
	----------
	input_sequence : A nucleotide sequence.  
	"""
	def __init__(self, input_sequence):
		self.seq = input_sequence

	def maskSequence(self, interval, toLower=False, maskingChar='N'):
		"""
		Masks the sequence based on the interval. 

		Parameters
		---------
		interval : A tuple containing the start and end positions for the masking. 
		toLower: If True, the sequence in the interval is converted to lower case bases.
						Default is False. 
		maskingChar :  Masking character. Default is 'N'.

		Returns
		-------
		Masked sequence.
		"""	
		sequence = self.seq
		start,end = interval

		if (toLower):
			return sequence[:start] + sequence[start:end].lower() + sequence[end:]
		else:
			return sequence[:start] + ''.join([maskingChar for x in range(end- start)]) + sequence[end:]


	def reverseComplement(self):
		"""
		Compute the reverse complement of a given sequence. 

		Returns
		-------
		sequence which is the reverse complement of the input sequence.
		"""	
		complementDict = {'A':'T', 'T':'A', 'G':'C', 'C':'G', 'N':'N'}
		result = ''
		for x in self.seq[::-1]:
			result += complementDict[x]
		return result	



















