import prompt
import custom_error

def enter(the_player):

	the_player.location = 'Row of houses'
	the_player.directions = ['Longer street','Suburb Junction']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:

		print "You're back at %s." % the_player.location
	else:
		the_player.visited.append(the_player.location)

		print "Just another street with rows of houses."
		print "This street ends with a right turn."


	while True:
		action = prompt.standard(the_player)

		if action == "longer street":
			return 'Suburb 3'
		elif action == "suburb junction" or 'junction' in action:
			return 'Suburb Junction'
		else:
			custom_error.errortype(3)
