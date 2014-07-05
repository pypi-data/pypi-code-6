import sys
import random
import prompt
import custom_error
import score
import fight
import death

def enter(the_player):
	the_player.location = 'Curling Street'
	the_player.directions = ['Apartment','Junction']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited and 'charlie sleepover' in the_player.visited and 'Wanda' in the_player.visited:
		print "\nThe whole Curling St. is swarmed with a herd of zombies."
		print "Wanda: 'Tss.. be careful."
		print "Here's the plan: I'm gonna sneak onto other side"
		print "and distract them."
		print "Meanwhile get in the shop and look for the motor - it should"
		print "have label 'K5-22TS' on it. It's pretty heavy so you might need"
		print "something to move it around."
		print "We'll meet back at Junction once you're done but be quick!'"

		score.calculate(the_player,'wanda decoy')
		
		print "\nWanda sneaks behind the cars and gets about 30m away from you."
		print "'Come on, you fuckers!' she screams. The herd starts moving towards"
		print "her. You hope she'll be fine."
		print "'B&D Motors' is ahead, you carefully sneak into the shop..."

		custom_error.errortype(4)

		return 'Motor Shop'

	elif the_player.location in the_player.visited and 'charlie sleepover' in the_player.visited:
		print "You try to step carefully, hiding behind close by dumpster."
		print "Unfortunately you step on broken glass and the"
		print "swarm starts to navigate towards you..."

		custom_error.errortype(4)

		while True:
			encounter = fight.Encounter(the_player, 'zombie male')
			encounter.start(the_player)
			print "As you finished one zombie, another one approaches."
			print "Time to get ready..."

			custom_error.errortype(4)

	elif 'motor' in the_player.inventory.keys() and 'Wanda' in the_player.visited:
		print "Wanda: 'We already got what we need, let's just go"
		print "the herd might move back here again.'"
		return 'Junction'

	elif the_player.location in the_player.visited:

		if 'gun' in the_player.inventory.keys():
			pass		

		else:
			print "There is still a policeman lying on the floor."
			pass
	
		print "You're in %s again." % the_player.location
		print "You've been here before."

		pass		
	
	else:

		the_player.visited.append(the_player.location)

		print "You walk out of your apartment."
		print "You are on %s, it's a large street" % the_player.location
		print "with junction at the end."
		print "There are corpses everywhere, all of them"
		print "are dead and didn't turn."
		print "Most of them probably commited suicide."
		print "You notice a corpse of policeman few meters from you."
	
	while True:
		if the_player.hitpoints <= 0:
			death.type(3, the_player)
		else:
			pass

		action = prompt.standard(the_player)

		if action == "apartment":
			return the_player.directions[0]
			break
		elif action == "policeman" and not 'gun' in the_player.inventory.keys():
			bullets = random.randint(5,10)
			the_player.inventory['gun'] = bullets
			print "You take the gun which has %d bullets in it." % bullets
			get_score = score.calculate(the_player, 'gun')
		elif action == "policeman":
			print "You already searched the policeman."
		elif action == "junction":
			return 'Junction'
		else:
			custom_error.errortype(3)

	