import prompt
import custom_error

def enter(the_player):

	the_player.location = 'Street with small houses'
	the_player.directions = ['Suburb Junction','A very long street']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:

		print "You're back at %s." % the_player.location
	else:
		the_player.visited.append(the_player.location)

		print "You come to street that has a lot"
		print "of small houses on both sides."
		print "It's uncanny how similar they are."
		print "There's a long street coming up ahead, Junction"
		print "behind you."

	while True:
		action = prompt.standard(the_player)

		if action == "suburb junction" or action == "junction":
			return 'Suburb Junction'
		elif action == "a very long street" or 'long' in action:
			return 'A very long street'
		else:
			custom_error.errortype(3)
