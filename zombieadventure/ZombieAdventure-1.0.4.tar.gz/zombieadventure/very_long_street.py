import prompt
import custom_error

def enter(the_player):

	the_player.location = 'A very long street'
	the_player.directions = ['Suburbs','Street with small houses']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:

		print "You're back at %s." % the_player.location
	else:
		the_player.visited.append(the_player.location)

		print "Nothing special about this street"
		print "except that it's really long."
		print "When you get to the end you"
		print "get a familiar sight in front of you."

	while True:
		action = prompt.standard(the_player)

		if action == "suburbs":
			return 'Suburbs'
		elif action == "street with small houses" or 'small houses' in action:
			return 'Street with small houses'
		else:
			custom_error.errortype(3)
