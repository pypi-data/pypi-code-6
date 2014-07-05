import random

def errortype(error_id):

	if error_id == 0:
		print "\nI do not understand\n"
	elif error_id == 1:
		print "\nPut down numbers only\n"
	elif error_id == 2:
		raw_input("\nPress any key to start over\n")
	elif error_id == 3:
		 print random.choice(["Wrong input","I do not understand this","Does not compute","Try something else"])
	elif error_id == 4:
		raw_input("\nPress ENTER key to continue\n")
	elif error_id == 5:
		print "\nPlease type in 'Y' or 'N' only.\n"
	else:
		pass 