import prompt
import fight
import score
import custom_error

def enter(the_player):

	if 'Wanda' in the_player.visited:
		the_player.location = 'Wanda\'s boat'
	else:
		the_player.location = 'Yellow boat'

	the_player.directions = ['Marina']

	print "\nLocation:", the_player.location
	print "-" * 30

	if 'zombie captain' not in the_player.visited:

		print "Looks like a habitant of Marina has turned."
		print "You see funny looking dead in striped shirt"
		print "and captain's hat... but boy he's ripped"
		print "as hell..."

		custom_error.errortype(3)

		encounter = fight.Encounter(the_player,'zombie captain')
		encounter.start(the_player)

		the_player.visited.append('zombie captain')

	else:
		pass


	if 'Wanda' in the_player.visited:
		if the_player.location in the_player.visited:
			print "You're back at %s." % the_player.location
			print "Wanda: 'OK, let's get this thing going.'"
		else:
			the_player.visited.append(the_player.location)

			print "Wanda: 'So this is the boat that me and"
			print "Dave found.'"

			print "You both inspect the ship and see that the"
			print "motor is indeed missing. Also the boat"
			print "needs special key to operate."
	else:
		pass

	if the_player.location in the_player.visited:
		print "You're back at the %s." % the_player.location


	else:
		the_player.visited.append(the_player.location)
		print "You inspect the boat and notice that the motor is missing."
		print "Also you need special key to operate the boat."


	while True:
		
		action = prompt.standard(the_player)

		if 'motor' in action and 'motor' in the_player.inventory.keys():
			print "You install the motor onto the boat. There seems to"
			print "be enough fuel left in tanks. Now all you need"
			print "is to start the motor."

			the_player.visited.append('motor installed')
		elif 'start' in action or 'key' in action or 'boat key' in action:
			print "You put the boat key in the ignition."

			if 'motor installed' in the_player.visited:
				print "You hear the motor start."
				score.calculate(the_player,'end game')
				custom_error.errortype(4)
				return 'Ending'
			else:
				print "Nothing happens, the motor is still missing."
		elif action == "marina":
			return 'Marina'
		else:
			custom_error.errortype(3)