import prompt
import custom_error
import fight

def enter(the_player):

	the_player.location = 'March Street'
	the_player.directions = ['Junction','Old building','Harrington River']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:

		print "You come back to %s. You've been here before." % the_player.location
		print "Old building is on your left side, ahead is Junction"
		print "of Curling Street"

		if 'charlie sleepover' in the_player.visited:
			print "You hear a very distant noise, probably coming"
			print "from Junction of Curling Street."
		else:
			pass

	else:
		the_player.visited.append(the_player.location)

		print "You leave junction of Curling Street behind"
		print "and turn right to %s." % the_player.location
		print "You see something moving towards you and feel"
		print "uneasiness and chill in your spine."

		encounter = fight.Encounter(the_player, 'child zombie')
		encounter.start(the_player)

		print "You successfully killed the enemy. Now you can safely"
		print "look around."
		print "Just by the sidewalk is an old building with grey walls."
		print "It is a three story building and there's a little light"
		print "coming out of the top window."
		print "Most of the windows, especially in ground floor are boarded up."
		print "If you continue walking you will end up near Harrington River."
		print "You can also turn back to Junction of Curling Street."

	while True:
		action = prompt.standard(the_player)

		if action == "junction":
			return 'Junction'
		elif action == "old building":
			return 'Old Building'
		elif action == "harrington river":
			return 'Harrington River'
		else:
			custom_error.errortype(3)

	