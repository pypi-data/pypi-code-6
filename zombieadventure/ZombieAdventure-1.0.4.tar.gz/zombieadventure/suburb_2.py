import prompt
import custom_error

def enter(the_player):

	the_player.location = 'Regular street'
	the_player.directions = ['Suburbs','Shorter street']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:

		print "You're back at %s." % the_player.location
	else:
		the_player.visited.append(the_player.location)

		print "Just another street with rows of houses."
		print "There is basically same street up ahead"
		print "but a little shorter."


	while True:
		action = prompt.standard(the_player)

		if action == "suburbs":
			return 'Suburbs'
		elif action == "shorter street":
			return 'Suburb 4'
