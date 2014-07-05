import prompt
import custom_error

def enter(the_player):

	the_player.location = 'Street with large mansion'

	if 'Wanda' in the_player.visited:
		the_player.directions = ['Suburb Junction','Wanda\'s house']
	else:
		the_player.directions = ['Suburb Junction','Mansion']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:

		print "You're back at %s." % the_player.location
	else:
		the_player.visited.append(the_player.location)

		print "Dog barking gets louder and you can"
		print "tell the sound is coming from a large"
		print "house at the end of the street."

	while True:
		action = prompt.standard(the_player)

		if action == "suburb junction" or action == "junction":
			return 'Suburb Junction'
		elif 'house' in action or 'mansion' in action:
			return 'Wandas House'
		else:
			custom_error.errortype(3)
