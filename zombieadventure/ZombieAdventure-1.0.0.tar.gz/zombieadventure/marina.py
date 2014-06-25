import prompt
import death
import custom_error

def enter(the_player):

	the_player.location = 'Marina'
	if 'Wanda' in the_player.visited:
		the_player.directions = ['Harrington River','Wanda\'s boat']
	else:
		the_player.directions = ['Harrington River','Yellow boat']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:
		print "You're back at %s." % the_player.location
		print "You see two smaller boats and %s." % the_player.directions[1]

	else:
		the_player.visited.append(the_player.location)

		print "You come to little Marina and notice two small"
		print "boats with paddle and larger yellow boat."

		if 'Wanda' in the_player.visited:
			print "Wanda: 'That yellow boat is the one!'"
		else:
			pass


	while True:

		action = prompt.standard(the_player)

		if action == "river" or action == "harrington river":
			return 'Harrington River'
		elif 'yellow' in action or 'boat' in action or 'wanda\'s boat' in action:
			return 'Wanda\'s boat'
		elif action == "small boat" or action == "small boats":
			print "One of the small boats is half-sunken and the other"
			print "looks crappy too. There are also no paddles."
		else:
			custom_error.errortype(3)