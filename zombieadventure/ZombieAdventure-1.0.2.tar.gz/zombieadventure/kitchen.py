import random
import prompt
import score
import custom_error

def enter(the_player):

	the_player.location = 'Kitchen'

	the_player.directions = ['Hallway of the house']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:
		print "You're back at %s." % the_player.location
		print "There are several shelves and four cupboards"
		print "above the sink."

	else:
		the_player.visited.append(the_player.location)

		print "You step into a kitchen. It looks like"
		print "it's been raided."

		if 'Wanda' in the_player.visited:
			print "Wanda: 'We've been here before with"
			print "Dave to get some food.'"
		else:
			pass
		
		print "There are several shelves and four cupboards"
		print "above the sink."

	cupboard = 1

	while True:
		
		action = prompt. standard(the_player)

		if 'house' in action or 'out' in action or 'hallway' in action:
			return 'House with pirate flag'
		elif 'cupboard' in action:
			print "You search one of the cupboards..."
			cupboard = cupboard + 1
			if cupboard == 4 and 'gun' in the_player.inventory.keys():
				print "You find some bullets for the gun!"
				the_player.inventory['gun'] = the_player.inventory['gun'] + 5
				score.calculate(the_player,'bullets')
			else:
				print "...and nothing. Maybe try looking in the other one?"
		elif 'shelves' in action or 'shelf' in action:
			print "Nothing in the shelves."
		else:
			custom_error.errortype(3)
