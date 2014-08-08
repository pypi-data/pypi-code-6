"""This is the "nester.py" module"""
def druk(lista):
	"""This function 
	is essential"""
	for each in lista:
		if isinstance(each,list):
			druk(each)
		else:
			print(each)
