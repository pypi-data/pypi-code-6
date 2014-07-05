import prompt
import custom_error

def enter(the_player):

	the_player.location = 'Shorter street'
	the_player.directions = ['Regular street','Street with a tree','House with pirate flag']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:

		print "You're back at %s." % the_player.location
		print "There's the house with the pirate flag."
	else:
		the_player.visited.append(the_player.location)

		print "The street is very similar to the one"
		print "You came from, except that you notice"
		print "there's a pirate flag on one of the"
		print "houses."
		print "You hear a distant dog bark."
		print "Up ahead you see that there's a tree"
		print "in next street."


	while True:
		action = prompt.standard(the_player)

		if action == "regular street":
			return 'Suburb 2'
		elif action == "street with a tree" or 'tree' in action:
			return 'Suburb 6'
		elif 'pirate' in action or 'flag' in action:
			return 'House with pirate flag'
		else:
			custom_error.errortype(3)
