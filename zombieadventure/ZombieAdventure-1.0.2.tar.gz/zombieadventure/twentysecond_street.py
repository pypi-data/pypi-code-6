import random
import prompt
import custom_error
import fight

def enter(the_player):

	the_player.location = '22nd Street'
	the_player.directions = ['Junction','Suburbs']

	print "\nLocation:", the_player.location
	print "-" * 30

	chance_of_encounter = random.randint(0,1)

	if chance_of_encounter == 1:
		print "You hear growling... Looks like"
		print "an enemy stumbled upon you.\n"
		encounter = fight.Encounter(the_player,'random')
		encounter.start(the_player)
		random.seed(chance_of_encounter)
	else:
		pass

	if the_player.location in the_player.visited:

		print "Your at %s again." % the_player.location

	else:
		the_player.visited.append(the_player.location)
		
		print "You come to %s, it looks empty here." % the_player.location
		print "If you continue going forward, you'll"
		print "reach Suburbs of Welton."


	while True:
		action = prompt.standard(the_player)

		if action == "suburbs":
			return 'Suburbs'
		elif action == "junction":
			return 'Junction'
		else:
			custom_error.errortype(3)





