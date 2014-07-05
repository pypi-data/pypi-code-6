import prompt
import custom_error
import fight

def enter(the_player):

	the_player.location = 'House with pirate flag'

	if the_player.location in the_player.visited and 'dog in pirate house' in the_player.visited:
		the_player.directions = ['Shorter street','Room with dead dog','Kitchen','Basement']
	elif the_player.location in the_player.visited and 'dog in pirate house' not in the_player.visited:
		the_player.directions = ['Shorter street','Left door','Right door','Stairs']
	else:
		the_player.directions = ['Shorter street','Left Door','Kitchen','Stairs']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:

		print "You're back at %s." % the_player.location
		print "There's a %s on your left, %s on your right" % (the_player.directions[1], the_player.directions[2])
		print "and stairs leading to %s." % the_player.directions[3]
	else:
		the_player.visited.append(the_player.location)

		print "It smells really bad in here. From where"
		print "you stand you see two doors, one on the"
		print "right and one on the left."
		print "You hear loud barking coming from behind"
		print "the left door."
		print "There are stairs leading down at the end"
		print "of the hall."
		print "Door behind you leads out to the street."


	while True:
		action = prompt.standard(the_player)

		if action == "shorter street" or 'shorter' in action or 'out' in action:
			return 'Suburb 4'
		elif 'left' in action or 'dog' in action:
			if 'dog in pirate house' not in the_player.visited:
				print "You open the wooden doors and angry dog jumps at you!"

				encounter = fight.Encounter(the_player,'infected dog')
				encounter.start(the_player)
				the_player.visited.append('dog in pirate house')

				print "There is nothing interesting in that room so you go out."
			else:
				print "Nothing here just the dead dog. You return to the hall."
		elif 'stairs' in action or 'basement' in action:
			return 'Basement'
		elif 'right' in action or 'kitchen' in action:
			return 'Kitchen'
		else:
			custom_error.errortype(3)