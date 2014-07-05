import prompt
import custom_error

def enter(the_player):

	the_player.location = 'Suburb Junction'

	if 'Wanda' in the_player.visited:
		the_player.directions = ['Street with a tree',
								'Row of houses',
								'Street with small houses',
								'Wanda\'s house street']

	else:
		the_player.directions = ['Street with a tree',
								'Row of houses',
								'Street with small houses',
								'Street with large mansion']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:

		print "You're back at %s." % the_player.location
		print "Everything looks normal here."
	else:
		the_player.visited.append(the_player.location)

		print "You enter a junction with the same houses"
		print "around. You can go to:"
		print "%s." % ','.join(the_player.directions)
		print "You're not sure where to go but you hear"
		print "louder dog barking from the direction"
		print "of Street with a large mansion."

	while True:
		action = prompt.standard(the_player)

		if action == "street with a tree" or 'tree' in action:
			return 'Suburb 6'
		elif action == "row of houses" or 'row' in action:
			return 'Suburb 5'
		elif action == "street with small houses" or 'small houses' in action:
			return 'Small houses'
		elif action == "street with large mansion" or 'mansion' in action or 'wanda' in action:
			return 'Cherry trees'
		else:
			custom_error.errortype(3)