import prompt
import score

def enter(the_player):

	the_player.location = 'Apartment'
	the_player.directions = ['Curling Street']

	print "\nLocation: ", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:
		print "You've been here already. It's your old"
		print "apartment."

	elif not the_player.location in the_player.visited:
		the_player.visited.append(the_player.location)
		print "You wake up at your old apartment."
		print "All the food and water is gone"
		print "and you know you've been postponing"
		print "your leave."
		print "The cupboard in the kitchen seems empty."
		print "You can go out to %s." % the_player.directions[0]

	else:
		pass


	while True:
		action = prompt.standard(the_player)

		if action == 'curling street' and not the_player.directions[0] in the_player.visited:
			print "You take courage and step out of your apartment."
			score.calculate(the_player, 'out of the house')
			break

		elif action == 'curling street' and the_player.directions[0] in the_player.visited:
			break

		elif action == 'cupboard' and not 'chocolate bar' in the_player.inventory.keys():
			print "You take a look once again, scanning"
			print "through empty packaging..."
			print "You find a chocolate bar!"

			the_player.inventory['chocolate bar'] = 1
			score.calculate(the_player, 'chocolate bar')

		elif action == 'cupboard':
			print "You search cupboard again but it's empty."

		else:
			pass

	return 'Curling Street'


	