import prompt
import custom_error

def enter(the_player):

	the_player.location = 'Street with a tree'
	the_player.directions = ['Shorter street','Suburb Junction']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:

		print "You're back at %s." % the_player.location
		print "The tree is still standing there"
		print "so nothing's changed."

	else:
		the_player.visited.append(the_player.location)

		print "You come to another street, again it's"
		print "very suburbish but you take a note"
		print "of an oak tree on side of the road."
		print "This street ends with a left turn."


	while True:
		action = prompt.standard(the_player)

		if action == "shorter street":
			return 'Suburb 4'
		elif action == "suburb junction" or action == "junction":
			return 'Suburb Junction'
		elif 'tree' in action:
			print "You come to the tree and see W + D carved into it."
		else:
			custom_error.errortype(3)
