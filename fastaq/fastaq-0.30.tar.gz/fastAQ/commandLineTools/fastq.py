import sys

input_file = sys.argv[1]

##### FASTA File
if (input_file.endswith('fastq')):
	from fastAQ.fastqInfo import FastqParser
	out = FastqParser(input_file)

	### Print sequence names
	def seqNames():
		return out.seqNames()

	## Get sequences for the names in the file.
	def seq():
		try:
			nameFile = open(sys.argv[3])
		except:
			return "Error : Provide a file containing names of the sequences."	
		for line in nameFile:
			record = line.strip()
			print out.sequenceDict()[record]
		return ''	

		

	## Base Qualities
	def qual():
		try:
			nameFile = open(sys.argv[3])
		except:
			return "Error : Provide a file containing names of the sequences."	
		for line in nameFile:
			record = line.strip()
			print out.baseQualities()[record]
		return ''	
		


		

	##	Trimming given sequences accroding to the intervals.
	def trim():
		try:
			nameFile = open(sys.argv[3])
			intervalFile = open(sys.argv[4])
		except:
			return "Error : Sequence and/or intervals file missing."		
		for line1, line2 in zip(nameFile, intervalFile):
			record1 = line1.strip()
			record2 = eval(line2)
			byInterval = True
			print out.trimSeq(record1, byInterval, interval=record2)
		return ''	

		


	## Trim sequences in the file by Mott's algo.
	def mottTrim():
		try:
			nameFile = open(sys.argv[3])
			limitValue = sys.argv[4].split('=')[1]
		except:
			return "Error : Sequence file missing."	
	
		for line in nameFile:
			record = line.strip()
			print out.trimSeq(name=record, mott=True, limitValue=float(limitValue))
		return ''	
		

	## Trim sequences in the file by removing low quality bases. 
	def trimLowQuality():
		try:
			nameFile = open(sys.argv[3])
			qualityCutOff = sys.argv[4].split('=')[1]
		except:
			return "Error : Sequence file missing."	
		for line in nameFile:
			record = line.strip()
			print out.trimSeq(name=record, qualityCutOff = float(qualityCutOff))
		return ''	
		


	## Mask Sequences in the file.
	def mask():
		try:
			nameFile = open(sys.argv[3])
			intervalFile = open(sys.argv[4])
		except:
			return "Error : Sequence and/or intervals file missing."	
	
		for line1, line2 in zip(nameFile, intervalFile):
			record1 = line1.strip()
			record2 = eval(line2)	
			print out.maskSeq(name=record1, interval=record2)
		return ''	
		


	## reverse complement the sequences in the given file. 
	def reverseComplement():
		try:
			nameFile = open(sys.argv[3])
		except:
			return "Error : Provide a file containing names of the sequences."
	
		for line in nameFile:
			record = line.strip()
			print out.reverseComplement(record)
		return ''	
		

	# trim all the sequences according to the interval
	def trimAll():
		try:
			intervalStart = sys.argv[3].split('=')[1]
			intervalEnd = sys.argv[4].split('=')[1]
		except:
			return "Error : Interval for trimming mising."	

		interval = (int(intervalStart), int(intervalEnd))
		intervals = [interval for x in out.seqNames()]
		return out.trimAll(byInterval=True, intervals=intervals)

		


	## Mott trim all the sequences.
	def mottTrimAll():
		try:
			limitValue = sys.argv[3].split('=')[1]
		except:
			return "Error : limit Value missing."		
		return out.trimAll(mott=True, limitValue=float(limitValue))
		


	# trim low quality bases from all the sequences.
	def trimAllLowQuality():
		try:
			qualityCutOff = sys.argv[3].split('=')[1]
		except:
			return "Error : qualityCutOff missing."		
		return out.trimAll(float(qualityCutOff))
			


	# mask all the sequences.
	def maskAll():
		try:
			intervalStart = sys.argv[3].split('=')[1]
			intervalEnd = sys.argv[4].split('=')[1]
		except:
			return "Interval is missing."	
	
		interval = (int(intervalStart), int(intervalEnd))
		intervals = [interval for x in out.seqNames()]
		return out.maskAll(intervals)
		
	# reverse complment all the sequences.
	def reverseComplementAll():
		return out.reverseComplementAll()	


	optionsDict = {'-seqNames':seqNames, '-seq':seq, '-qual':qual, '-trim':trim, '-trimLowQuality':trimLowQuality,
	'-mottTrim':mottTrim, '-mask':mask, '-trimAll':trimAll, '-mottTrimAll':mottTrimAll, '-trimAllLowQuality':trimAllLowQuality,
	'-maskAll':maskAll, '-reverseComplement': reverseComplement, '-reverseComplementAll':reverseComplementAll}	


	#####Choose Options
	options = sys.argv[2]
	print optionsDict[options]()

















