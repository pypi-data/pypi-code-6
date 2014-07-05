import prompt
import custom_error
import score
import fight

def enter(the_player):

	the_player.location = 'Old Building (first floor)'
	the_player.directions = ['Old Building', 'Old Building (second floor)']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:

		dave = False

		print "You're on %s again. Dave's corpse is still here." % the_player.location
		print "You can go down in Old Building Lobby or up"
		print "in to second floor."

		if 'Wanda' in the_player.visited and 'Dave is dead' in the_player.visited:
			print "\nYou see Wanda turning away from Dave's body."
			print "'Let's go' she says."

		elif 'Wanda' in the_player.visited:
			print "\nWanda: 'My god... that's David... or what's left of him!'"
			print "She starts sobbing uncontrollably. You decide"
			print "that it's best if you just go."

		else:
			pass
	
	else:
		the_player.visited.append(the_player.location)

		dave = True

		print "You see that the light comes from the windows"
		print "that were not boarded up."
		print "You see a grafitti painted on eastern wall"
		print "saying 'DON'T GO UP!'."
		print "You go to near the window to look outside."
		print "You scan the horizon towards Curling Street"
		print "and see a pack of zombies coming towards you."
		print "You quickly step away from the window and"
		print "immediately hear growling breath behind you."
		print "You quickly turn around to see decomposed"
		print "guy in uniform." 
		print "He reminds you if pizza delivery boy"
		print "that you used to meet."

		custom_error.errortype(4)

		if 'Wanda' in the_player.visited:
			print "'DAVE!' Wanda shouts. 'Please let's leave him"
			print "alone!'"
		else:
			pass

		custom_error.errortype(4)

		print "It's weird. He has a leash on his neck and"
		print "he angrily swings his arm towards you,"
		print "clenching his teeth."
		print "You try to slide past him but pizza boy"
		print "snaps into amok."
		print "In one moment the rope on his leash snaps."
		print "Ooops..."

		custom_error.errortype(4)

		encounter = fight.Encounter(the_player, 'Dave')
		encounter.start(the_player)

		dave = False

		the_player.visited.append('Dave is dead')

		if 'Wanda' in the_player.visited:
			print "'Oh my what did we just do? ..."
			print "I guess it was necessary... but.."
			print "poor Dave. He didn't deserve this.'"
			custom_error.errortype(4)
		else:
			pass

		print "Breathing heavily you observe remains of this"
		print "familiar guy and notice a name tag on his"
		print "shirt. It says 'DAVE'."

	while True:
		action = prompt.standard(the_player)

		if action == "dave" and 'dave chocolate' in the_player.visited:
			print "There's not anything on Dave."

		elif action == "dave" and not 'dave chocolate' in the_player.visited:
			the_player.visited.append('dave chocolate')
			print "You quickly search Dave's body"
			print "and to your surprise you find"
			print "old chocolate but it still looks OK."

			if 'chocolate bar' in the_player.inventory.keys():
				print "Cool another chocolate bar."
				the_player.inventory['chocolate bar'] = the_player.inventory['chocolate bar'] + 1
				print "You have %d bars now." % the_player.inventory['chocolate bar']
				score.calculate(the_player, 'chocolate bar')
			elif 'chocolate bar' not in the_player.inventory.keys():
				the_player.inventory['chocolate bar'] = 1
				score.calculate(the_player, 'chocolate bar')
		elif action == "second floor" or action == "old building (second floor)":
			return 'Old Building (second floor)'
		elif action == "lobby" or action == "old building":
			return 'Old Building'
		else:
			custom_error.errortype(3)


