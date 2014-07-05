# -*- coding: utf-8 -*-

import prompt
import custom_error
import score
import death

def enter(the_player):

	the_player.location = 'Old Building'
	the_player.directions = ['March Street','Old Building (first floor)']

	print "\nLocation:", the_player.location
	print "-" * 30

	num_of_tries = 4

	if the_player.location in the_player.visited and 'flashlight' in the_player.inventory.keys():
		print "You turn on the flashlight. Suddenly you can see all"
		print "the dead bodies in the room."

		if 'first time flash light' in the_player.visited:
			print "You see the trunk."


		else:
			the_player.visited.append('first time flash light')
			score.calculate(the_player,'turn on lights')

			print "Apart from the horrendous scene you notice a large trunk"
			print "in the back of the room."
			print "You come closer to open it but discover that"
			print "it has a mechanical lock on it with three"
			print "cylinders with number on them."
			print "The trunk has letters 'AK' crudely painted on it."

			if 'Wanda' in the_player.visited:
				print "\nWanda: 'That trunk is where our stuff should be.'"


	elif the_player.location in the_player.visited:

		print "You are at the lobby of %s again. It's dark here." % the_player.location

	else:
		the_player.visited.append(the_player.location)

		print "It's very dark inside and the smell is horrible."
		print "You can't see anything but you see a little"
		print "light coming from the other side of the lobby."
		print "You see some stairs leading up to first floor."

		if 'Wanda' in the_player.visited:
			print "\nWanda: 'This is it, this is the building. The stuff"
			print "must be somewhere here.'"

	while True:
		action = prompt.standard(the_player)

		if action == "march street" or 'out' in action:
			return 'March Street'
		elif action == "stairs" or action == "first floor":
			return 'Old Building (first floor)'
		elif action == "trunk" and not 'map' in the_player.inventory.keys():

			if 'Wanda' in the_player.visited:
				print "\n'The code is 498 but be careful"
				print "because you only have few tries."
				print "There's a special poison needle"
				print "to avoid hassling with the lock'"
			else:
				pass

			while True:
				if num_of_tries != 0:
					try:
						passcode = int(raw_input("Enter three digits, '000' to go away > "))
						num_of_tries = num_of_tries - 1
					except ValueError:
						print "Put three numbers only"
					if passcode == 000:
						break
					elif passcode == 498:
						the_player.inventory['boat key'] = 1
						score.calculate(the_player, 'key')

						print "You find some junk inside but most importantly,"
						print "the key for the boat is there. It is squared-shaped"
						print "and kind of unique."

						if 'Wanda' in the_player.visited:
							print "Wanda: 'We got the key! Let's go.'"
						else:
							pass
						break
					else:
						print "It's still locked."
				else:
					death.type(9, the_player)


		else:
			custom_error.errortype(3)
			pass