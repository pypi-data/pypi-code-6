import prompt
import custom_error

def enter(the_player):

	the_player.location = 'Longer street'
	the_player.directions = ['Another street','Row of houses']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:

		print "You're back at %s." % the_player.location
		print "You still hear the dog barking."
	else:
		the_player.visited.append(the_player.location)

		print "Just another street."
		print "There is a street with row of houses ahead."
		print "On your right there's a patch of flowers"
		print "that isn't on other lawns."
		print "You hear barking from afar."


	while True:
		action = prompt.standard(the_player)

		if action == "another street":
			return 'Suburb 1'
		elif 'row' in action or 'houses' in action:
			return 'Suburb 5'
		elif action == "patch of flowers" or action == "flower":
			print "You smell the flowers. They smell nice."
			print "You look inside the house where the flowers"
			print "are but there's nothing special about it."
		else:
			custom_error.errortype(3)
