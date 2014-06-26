import random
import prompt
import score
import custom_error

def junk(the_player):
	
	dives = 0
	dive_messages = ["You fail to find anything.",
					"Still nothing",
					"You're looking but it's just junk.",
					"Useless junk",
					"Some crap you don't need.",
					"Some dusty thing",
					"Nothing interesting"]

	print "\nYou dive into the junk."

	while dives <= random.randint(8,15):

		chance = random.randint(1,6)
		map_chance = random.randint(1,8)
		dive = raw_input("ENTER to dive, 'S' to stop > ").lower()
		custom_error.errortype(4)

		if dive == "s":
			break
		else:
			dives = dives + 1

			if chance == 4 and 'baseball bat' not in the_player.inventory.keys():
				print '\nYou find a baseball bat!'
				the_player.inventory['baseball bat'] = 10
				score.calculate(the_player, 'baseball bat')
				break
			elif map_chance == 7 and 'map' not in the_player.inventory.keys():
				print "You find a map of the Suburbs!"
				the_player.inventory['map'] = 1
				score.calculate(the_player,'map')
				print "Type 'MAP' to display map."
				break
			else:
				print '\n', random.choice(dive_messages)

	print "\nYou're bored so you need to rest for a while."

def enter(the_player):

	the_player.location = 'Basement'

	the_player.directions = ['Hallway of the house']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:
		if 'flashlight' in the_player.inventory.keys():
			print "Back in the %s." % the_player.location
			print "Heaps of junk everywhere."
		elif 'flashlight' not in the_player.inventory.keys():
			print "You're back at %s but it's still dark here."
			print "You can't see anything."

	else:
		the_player.visited.append(the_player.location)

		if 'flashlight' in the_player.inventory.keys():
			print "Thankfully you have flashlight with you"
			print "so you turn it on."
			print "You're in some kind of a basement that"
			print "has brick walls. It's very humid here."
			print "There's a lot of junk laying around."


		elif 'flashlight' not in the_player.inventory.keys():
			print "You step into the darkness and listen for"
			print "a while. It's silent and very humid in here"
			print "but also no light available."

	while True:
		
		action = prompt. standard(the_player)

		if 'house' in action or 'out' in action or 'hallway' in action:
			return 'House with pirate flag'
		elif 'junk' in action:
			junk(the_player)
		else:
			custom_error.errortype(3)
