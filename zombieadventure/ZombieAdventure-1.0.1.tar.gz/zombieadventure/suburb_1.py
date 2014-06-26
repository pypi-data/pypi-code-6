import prompt
import custom_error

def enter(the_player):

	the_player.location = 'Another street'
	the_player.directions = ['Suburbs','Longer street']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:

		print "You're back at %s." % the_player.location
	else:
		the_player.visited.append(the_player.location)

		print "Just another street with rows of houses."
		print "Only difference is a slightly more"
		print "red mailbox next to one of the houses."
		print "There is a longer street up ahead."


	while True:
		action = prompt.standard(the_player)

		if action == "suburbs":
			return 'Suburbs'
		elif action == "longer street":
			return 'Suburb 3'
		elif action == "red mailbox" or action == "mailbox":
			print "You inspect the house but nothing of"
			print "interest is inside."
		else:
			custom_error.errortype(3)
