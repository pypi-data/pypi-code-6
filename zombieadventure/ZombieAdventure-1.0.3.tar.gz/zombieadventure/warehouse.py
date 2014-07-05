import string
import random
import prompt
import custom_error
import score


def shelf(the_player):


	shelves = [i for i in string.ascii_lowercase]
	shelves_view = ', '.join(shelves).upper()

	while True:
		
		print "\nShelves are labeled as:\n%s." % shelves_view

		try:
			select = str(raw_input("Type letter to inspect shelf, 'exit' to stop > ")).lower()

			if select == "exit":
				return 'Warehouse'
			elif select in shelves:
				single_shelf(select, the_player)
			else:
				custom_error.errortype(3)
				custom_error.errortype(4)
		except ValueError:
			print "Type letters only"

def single_shelf(shelf_id, the_player):

	compartments = []

	for item in range(1,6):
		compartment = shelf_id
		compartments.append((compartment, item))

	print "You come to shelf %s and see compartmens marked as:" % shelf_id.upper()
	
	for compartment in compartments:
		print compartment[0].upper() + str(compartment[1])

	while True:
		select = str(raw_input("Type letter and number to look into container, 0 to go back > ")).lower()

		if select == "0":
			break
		elif len(select) == 1:
			print "Please specify container."
		elif select == "t1" and shelf_id == "t" and 'motor' in the_player.inventory.keys():
			print "There is nothing else in that container."
		elif select == "t1" and shelf_id == "t":
			print "\nYou found the motor!"
			score.calculate(the_player, 'find motor')
			the_player.inventory['motor'] = 1
			
			if 'cart' in the_player.inventory.keys():
				print "You put the motor in the cart. You're ready to go!"
			else:
				print "You can carry the motor for few meters but it is very heavy."
				print "You're gonna need something for carrying it."
			custom_error.errortype(4)
			return 'Warehouse'
		elif select == "a2" and shelf_id == "a" and 'gun' in the_player.inventory.keys():
	
			if 'warehouse bullets' not in the_player.visited:
				bullets = random.randint(3,7)
				print "\nYou found %d bullets for gun." % bullets
				score.calculate(the_player,'bullets')
				the_player.inventory['gun'] = the_player.inventory['gun'] + bullets
				the_player.visited.append('warehouse bullets')
			else:
				print "\nThere is nothing else inside."
		elif select == "h4" and shelf_id == "h":
			print "You find a note:"
			print "'PUSH UP' to be the best."
			score.calculate(the_player,'easter egg')
			return 'Warehouse'
		elif select == "q2" and shelf_id == "q":
			print "You find a note:"
			print "'I wish I could write better code...' - author."
			score.calculate(the_player,'easter egg')
		elif shelf_id not in select:
			print "That container is not here."
		else:
			print random.choice(["It's empty.","There's some random junk inside","A weird steel thing!", "Nothing of interest."])

def enter(the_player):

	the_player.location = 'Warehouse'
	the_player.directions = ['Motor Shop']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:
		print "You're back at the warehouse of B&D Motor shop."

	else:
		the_player.visited.append(the_player.location)

		print "The door says 'Warehouse' and you"
		print "carefully approach it and open it."
		print "Inside is a large area that was intended"
		print "as a storage facility."
		print "You see multiple columns of shelves"
		print "with letters and numbers on them."

	while True:
		
		print "\nYou stand in front of the shelves, behind you"
		print "is a door leading to %s." % the_player.directions[0]
		
		action = prompt.standard(the_player)

		if action == "shelf" or action == "shelves":
			shelf(the_player)
		elif action == "motor" or action == "motor shop":
			return 'Motor Shop'
		else:
			custom_error.errortype(3)
			
