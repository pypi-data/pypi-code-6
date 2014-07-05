import random
import prompt
import score
import death
import fight
import custom_error

def container(the_player):

	containers = range(1,8)
	right_container = random.choice(containers)

	print "You go closer to the containers. There are"
	print "%d of them, all green. Which one do you want" % len(containers)
	print "to look at?"

	tries = 0
	right_tries = 0

	while True:
		
		try:
			print "Number (%d - %d), '0' to exit > " % (containers[0],containers[-1])
			choice = int(raw_input("> "))

			if choice in containers:
				if choice == right_container and right_tries == 2 and 'foreman knife' not in the_player.visited:
					print "You find a knife!"
					the_player.inventory['knife'] = 15
					score.calculate(the_player,'knife')
					the_player.visited.append('foreman knife')
				elif choice == right_container and right_tries == 0:
					print "Hmm.. maybe you need to look further."
					right_tries = right_tries + 1
				elif tries == 0:
					tries = tries + 1
					print "Hmm.. maybe you need to look further."
				elif choice == right_container and right_tries == 1:
					print "You need to go deeper..."
					right_tries = right_tries + 1
				elif tries == 1:
					print "You need to go deeper..."
					tries = tries + 1
				elif tries == 2:
					print "You find nothing."
					tries = 0
			elif choice == 0:
				break
			else:
				print "That container does not exist."
		except ValueError:
			print "Put down numbers only."

def enter(the_player):

	the_player.location = 'Foreman Ave'
	the_player.directions = ['Junction','Commercial Building', 'Car barricade']
	glass = random.randint(1,4)

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:
		print "You're back at %s." % the_player.location
		print "There are waste containers on the side"
		print "of the road."
		print "Building with broken shop window is next to them."

	else:
		the_player.visited.append(the_player.location)

		print "You come to wide street with various shops"
		print "on each side and garbage everywhere."
		print "There are seven green waste containers on the right"
		print "side of the road that are stuffed"
		print "with various things."
		print "You see a commercial building, probably a shop"
		print "with broken front shop window."
		print "The street ends with a huge barricade made out of"
		print "cars."

	while True:

		action = prompt.standard(the_player)

		if action == "junction":
			return 'Junction'
		elif 'waste' in action or 'container' in action:
			container(the_player)
		elif 'window' in action or 'commercial' in action or 'building' in action:
			if glass == 1:
				death.type(12,the_player)
			else:
				print "You lose balance while stepping to the shop,"
				print "you almost impale yourself on glass shrapnel."
				print "Don't try that again!"
				score.calculate(the_player,'glass')
		elif 'cars' in action or 'barricade' in action or 'car' in action:

			print "You try to climb the car barricade but"
			print "you fail, falling to the ground."
	
			if 'car barricade' not in the_player.visited:
				encounter = fight.Encounter(the_player,'random')
				print "Somehow, a zombie crawls from one of the cars."
				
				custom_error.errortype(4)
				encounter.start(the_player)
				the_player.visited.append('car barricade')
			else:
				pass
		else:
			custom_error.errortype(3)


