import prompt
import custom_error

def enter(the_player):

	the_player.location = 'Suburbs'
	the_player.directions = ['22nd Street','Left','Right']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:

		print "You've reached %s, you're standing in" % the_player.location
		print "one of the front streets."

	else:
		the_player.visited.append(the_player.location)

		print "Few minutes later you arrive to Welton"
		print "suburbs. The street you're on forks"
		print "into two roads (left and right)."
		print "In the distance you see many other roads"
		print "but everything looks so similiar."
		print "All the houses are same size and all"
		print "the lawns are green."
		print "Where do you go?"


	while True:
		action = prompt.standard(the_player)

		if action == "22nd street":
			return '22nd Street'
		elif action == "left":
			return 'Suburb 1'
		elif action == "right":
			return 'Suburb 2'
		else:
			custom_error.errortype(3)

