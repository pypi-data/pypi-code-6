import sys
import splashscreen
import custom_error

def enter(the_player):

	splashscreen.outro()

	print "\nAs you set sail you feel a peace, finally."
	print "You observe Welton as it gets further away from"
	print "you. You don't know where you'll end up"
	print "but as long as Wanda\'s with you,"
	print "you feel it's gonna be alright."
	print " \nTHE END"

	custom_error.errortype(4)
	
	splashscreen.score_board(the_player)
	
	custom_error.errortype(4)
	
	exit(1)
