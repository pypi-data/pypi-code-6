import sys

input_file = sys.argv[1]

##### FASTQ File
if (input_file.endswith('fasta')):
	from fastAQ.fastaInfo import FastaParser
	out = FastaParser(input_file)

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
			print out.trimSeq(record1, interval=record2)
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
			print out.maskSeq(record1, record2)
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
			intervalEnd  = sys.argv[4].split('=')[1]
		except:
			return "Error : Interval for trimming mising."	
		interval = (int(intervalStart),int(intervalEnd))
		intervals = [interval for x in out.seqNames()]
		byInterval = True
		return out.trimAll(intervals)
			



	# mask all the sequences.
	def maskAll():
		try:
			intervalStart = sys.argv[3].split('=')[1]
			intervalEnd  = sys.argv[4].split('=')[1]
		except:
			return "Interval is missing."	
		interval = (int(intervalStart),int(intervalEnd))	
		intervals = [interval for x in out.seqNames()]
		return out.maskAll(intervals)
			

	# reverse complment all the sequences.
	def reverseComplementAll():
		return out.reverseComplementAll()	


	optionsDict = {'-seqNames':seqNames, '-seq':seq, '-trim':trim, '-mask':mask, '-trimAll':trimAll, 
	'-maskAll':maskAll, '-reverseComplement': reverseComplement, '-reverseComplementAll':reverseComplementAll}	


	#####Choose Options
	options = sys.argv[2]
	print optionsDict[options]()

















