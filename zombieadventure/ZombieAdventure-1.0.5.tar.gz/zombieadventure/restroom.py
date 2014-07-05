import custom_error
import prompt

def enter(the_player):

	the_player.location = 'Restroom'
	the_player.directions = ['Maintenance room']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:
		print "At restroom again."

	else:
		the_player.visited.append(the_player.location)

		print "You're in very little room with toilet"
		print "and sink in it. It is pretty crammed in"
		print "here."

	if 'broom' in the_player.inventory.keys():
		print "The door behind you lead back to %s." % the_player.directions[0]

	elif 'broom' not in the_player.inventory.keys():
		print "There's an old broom with steel handle"
		print "leaning on the wall."


	while True:
		

		action = prompt.standard(the_player)

		if action == "maintenance room" or action == "maintenance" or 'out' in action:
			return 'Maintenance room'
		elif "broom" in action:
			if 'broom' not in the_player.inventory.keys():
				print "You take the broom, it looks like it might"
				print "be useful for something."

				the_player.inventory['broom'] = 1
			else:
				print "You already have the broom."
		elif 'toilet' in action:
			print "You don't feel like going."
		else:
			custom_error.errortype(3)