import prompt
import death
import custom_error

def enter(the_player):

	the_player.location = 'Harrington River'
	the_player.directions = ['March Street','Marina','Bridge']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:
		print "You're back at %s." % the_player.location

	else:
		the_player.visited.append(the_player.location)
		print "The March Street ends abruptly with a large"
		print "parking lot in front of Harrington River."
		print "There is a wooden bridge that overarches the river"
		print "so you can keep going."
		print "A narrow stairwell-like path leads to river's"
		print "edge where small marina is located along"
		print "with couple of boats."

	while True:

		action = prompt.standard(the_player)

		if "bridge" in action:
			print "You step on the bridge and hear loud"
			print "cracking beneath your feet."

			bridge_prompt = raw_input("Continue? Y/N > ").lower()

			if bridge_prompt == "y":
				death.type(11, the_player)
			else:
				pass

		elif 'stairs' in action or 'path' in action or 'marina' in action:
			return 'Marina'
		elif action == "march street":
			return 'March Street'
		else:
			custom_error.errortype(3)


