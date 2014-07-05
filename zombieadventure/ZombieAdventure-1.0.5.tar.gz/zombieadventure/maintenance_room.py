import custom_error
import prompt
import score
import fight

def workbench(the_player):

	print "You're at huge wooden workbench with some tools around."
	print "You inspect your stuff if you can make something useful,"

	cart_items = ['wheels','wooden board','broom']
	available_items = []

	for item in cart_items:
		if item in the_player.inventory.keys():
			available_items.append(item)
		else:
			pass

	
	if available_items == []:
		print "but you don't know what to do."
	elif 'cart' in the_player.inventory.keys():
		print "You've already built the cart so there's no need to mess around."
	else:
		print "and seems like %s is useful." % ' and '.join(available_items[0:len(available_items)])

		if 'wheels' in available_items and 'wooden board' in available_items and 'broom' in available_items:
			print "\nGreat! You create a box from wooden boards and then you nail"
			print "the bicycle wheels onto it. You use the broom stick as a lever"
			print "so you can push it. You've created a carrying cart!"

			del the_player.inventory['wheels']
			del the_player.inventory['wooden board']
			del the_player.inventory['broom']

			the_player.inventory['cart'] = 1
			score.calculate(the_player,'cart')
		elif 'wheels' in available_items and 'wooden board' in available_items:
			print "You get an idea to create a box from wooden boards and attach"
			print "the bicycle wheels but you still need some kind of lever"
			print "to push it."
		elif 'wheels' in available_items and 'broom' in available_items:
			print "You've got wheels and broom but there is still something missing."
		elif 'broom' in available_items and 'wooden board' in available_items:
			print "You can try to build a box from wooden boards and attach"
			print "the broom stick, but still the thing will be unmovable."
		elif 'wheels' in available_items:
			print "You've got two wheels but you need some kind of box"
			print "made from some solid material so you can put stuff in it."
		elif 'wooden board' in available_items:
			print "Your wooden boards can be made into a box. It's nice for starters"
			print "but you need to move it somehow."
		elif 'broom' in available_items:
			print "Your broom can be disassembled and the handle will be useful"
			print "as a lever. On its own it doesn't do much."
			print "There is one more thing missing."
		else:
			pass

def enter(the_player):

	the_player.location = 'Maintenance room'
	the_player.directions = ['Motor Shop', 'Restroom']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:
		print "You're back at the %s." % the_player.location

	else:
		the_player.visited.append(the_player.location)

		print "You open the door and something immediately jumps at you!"

		custom_error.errortype(4)

		the_player.visited.remove('Wanda')

		encounter = fight.Encounter(the_player, 'random')
		encounter.start(the_player)

		the_player.visited.append('Wanda')

		print "That was close!"

	print "In front of you, you see lots of junk. There is a closet on the left"
	print "and next to it is some kind of workbench."
	print "There are also paper boxes and wooden crates around the place."
	print "On your right you see doors marked 'restroom'."

	while True:
		
		action = prompt.standard(the_player)

		if action == 'restroom' or 'rest' in action:
			return 'Restroom'
		elif action == "closet":
			if 'wheels' in the_player.inventory.keys():
				print "There isn't anything useful in there anymore."
			else:
				print "You find some spare bike parts. Everything looks functional"
				print "and the wheels might be useful for something so you take them."
				the_player.inventory['wheels'] = 2
		elif action == "workbench":
			workbench(the_player)
		elif action == "paper boxes" or action == "boxes":
			print "You don't find anything useful."
		elif action == "wooden crates" or action == "crates" or action == "crate":
			if 'wooden board' in the_player.inventory.keys():
				print "The crates are already disassembled and there is"
				print "nothing of use to you."
			else:
				print "You inspect wooden crates and nothing if interest"
				print "is inside them, just some random junk."
				print "But the crates themselves are made of wooden boards"
				print "that you think you could use."
				print "You take few of the crates apart and get several boards."
				the_player.inventory['wooden board'] = 5
		elif action == "motor shop" or action == "shop":
			return 'Motor Shop'
		else:
			custom_error.errortype(3)
