import prompt
import custom_error
import death

def enter(the_player):

	the_player.location = 'Wanda\'s house'

	if 'Wanda' in the_player.visited:
		the_player.directions = ['Wanda\'s house street']
	else:
		the_player.directions = ['Street with large mansion']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:

		print "You've come back to %s." % the_player.location
		print "Alfie greets you by jumping at you."

	else:
		the_player.visited.append(the_player.location)

		print "The door were not locked but as soon"
		print "as you got inside you see the dog"
		print "that was making all the noise."
		print "The dog is a large dachshund with"
		print "really threatening look."
		print "It's growling at you..."

		custom_error.errortype(4)

		print "Suddenly you hear 'Alfie!' and"
		print "the dog runs up the wooden stairs."
		print "There you see a young woman aiming"
		print "small revolver at you."
		print "She says: 'Now I'm going"
		print "to ask you some questions and you're'"
		print "gonna answer.'"

		custom_error.errortype(4)

		end_conversation = False

		while end_conversation == False:

			print "'Are you gonna hurt me?'"
			print "1. Yes"
			print "2. No\n"

			answer_hurt = prompt.conversation()

			if answer_hurt == 1:
				death.type(10,the_player)
			elif answer_hurt == 2:
				print "'Good, good."
				print "Why did you come here?'"

				while end_conversation == False:
					print "1. I was looking for a shelter."
					print "2. I heard the dog barking."
					print "3. I need to get out of this town.\n"

					answer_come = prompt.conversation()

					if answer_come == 2:
						print "'Hmm. Alfie's been tense lately'"
						print "and this is exactly what I was worried"
						print "about. That the barking would attract more"
						print "deads or not-so-friendly types.'\n"

						pass

					elif answer_come == 1:
						print "Well... you can't expect me to offer you"
						print "a place to crash. You're a stranger!\n"

						pass

					elif answer_come == 3:
						end_conversation = True

			else:
				custom_error.errortype(1)

		print "'Well.. that makes two of us... name's Wanda by the way.'"
		print "'%s' you say." % the_player.name
		print "'Nice to meet you.'"

		custom_error.errortype(4)

		print "'Listen, I have a plan, sort of. Me and my boyfriend"
		print "were staying at this building on March St. We were"
		print "preparing to get outta town."
		print "We had everything - supplies, ammo and a ride..."
		print "but then a horde of deads heard us and started to"
		print "crawl into the lobby.'"

		custom_error.errortype(4)

		print "Well I managed to escape and still.. a herd of them"
		print "were following me for days. Then I found this place"
		print "and I have been here since."
		print "I couldn't get back... I was so scared and I'm not sure"
		print "I'll even see Dave again..."

		if 'Dave is dead' in the_player.visited:

			print "You: 'Listen, Wanda..'"
			print "'I know what happened to Dave.'"
			print "Wanda: 'You saw him?!'"
			print "'Yeah.. he turned, I had to kill him,' you replied."
			print "Wanda explodes in tears, you try to comfort her"
			print "but it's useless"

			custom_error.errortype(4)

			print "Few hours later she calms down a bit."
			print "'Hey.. I can't stay here. I gotta get away."
			print "let's get back to what I was trying to say...'"

		else:
			pass

		print "\n'The really bad thing is we had a perfect way out."
		print "We managed to fix one of the boats on Harrington River"
		print "but it had a broken motor.'"
		print "\n'So we got found a new one in a shop on Curling Street.'"
		print "You: 'Yeah that's where my place is.'"
		print "'Cool. But it gets worse. The keys for the boat"
		print "are somewhere in the building on March St., the place"
		print "where I saw Dave for last time.'"

		custom_error.errortype(4)

		print "'There should be a trunk with lock on it, I have the"
		print "password.'"
		print "\n'Let's get the motor and the key and get out of this"
		print "hellhole."
		print "We'll get going tomorrow morning.'"

		custom_error.errortype(4)

		hp_to_heal = the_player.max_hitpoints - the_player.hitpoints
		the_player.hitpoints = the_player.hitpoints + hp_to_heal
		print "You gain %.1f hitpoints from good night sleep.\n" % hp_to_heal


		print "'Hey %s here you go. It's a bandage that'll" % the_player.name
		print "heal you but it takes time to apply so you"
		print "need to use it outside of battle.'"
		print "\n*** Type HEAL outside of battle to heal yourself. ***\n"

		the_player.inventory['bandage'] = 2

		print "You get %d bandages." % the_player.inventory['bandage']
		print "Let's go! Alfie you need to stay here for now."

		the_player.visited.append('Wanda')


	while True:
		action = prompt.standard(the_player)

		if action == "street with large mansion" or 'out' in action or 'street' in action:
			return 'Cherry trees'
		else:
			custom_error.errortype(3)

