import prompt
import custom_error

def enter(the_player):

	the_player.location = 'Junction'
	the_player.directions = ['Curling Street','March Street', '22nd Street', 'Foreman Ave']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:

		print "You're back at %s of Curling Street again." % the_player.location
		print "You've been here before."
	
		if the_player.location in the_player.visited and 'charlie sleepover' in the_player.visited:
			print "The sound is definitely coming from Curling Street."
		else:
			pass

	else:
		the_player.visited.append(the_player.location)

		print "You pass few building in Curling Street"
		print "carefully. Thankfully no zombies are present here."
		print "Behind you is Curling Street, on your right"
		print "you can go to March Street, on your left"
		print "there's 22nd Street."
		print "If you continue to go forward you will enter Foreman Ave."

	while True:
		action = prompt.standard(the_player)
		
		if action == "curling street" and 'got the motor' in the_player.visited:
			print "The zombies are still herding in Curling Street and"
			print "you've already got what you need."

		elif action == "curling street" and 'charlie sleepover' in the_player.visited and 'Wanda' in the_player.visited:
			print "From afar you see a herd of zombies scattered in the street."
			print "Wanda: 'Let's go I have a plan.'"

			custom_error.errortype(4)
			return 'Curling Street'

		elif action == "curling street" and 'charlie sleepover' in the_player.visited:
			print "You go few meters but after a while you notice zombie sounds."
			print "A swarm of deads is scattered around the whole Curling Street."
			print "It doesn't look like a good idea to go there"
			print "but if you really want you might give it a shot:\n"

			while True:
				go_to_swarm = raw_input("> Continue? Y/N").lower()
				if go_to_swarm == "y":
					return 'Curling Street'
				elif go_to_swarm == "n":
					print "You decide to return to junction."
					break
				else:
					print "Type only 'Y' or 'N'."

		elif action == "curling street":
			return 'Curling Street'
		elif action == "march street":
			return 'March Street'
		elif action == "22nd street":
			return '22nd Street'
		elif action == 'foreman ave' or action == "foreman avenue":
			return 'Foreman Ave'
		elif action == 'knife':
			the_player.inventory['knife'] = 50
			print "You pick up knife"
		else:
			custom_error.errortype(3)