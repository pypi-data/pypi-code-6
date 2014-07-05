import custom_error
import prompt
import score

def laptop(the_player):

	computer = True

	while computer:
		
		print "\n--- Welcome to ShopDB ver. 3.0 ---"
		print "\nPlease select number, type '0' to log out:"
		print "1. Browse inventory"
		print "2. Billings"
		print "3. Employees"


		computer_prompt = int(raw_input("> "))

		if computer_prompt == 1:

			computer2 = True
			
			while computer2:

				print "\n1. Axx - Gxx"
				print "2. Hxx - Oxx"
				print "3. Mxx - Zxx"
				print "4. <- back"

				computer_prompt2 = int(raw_input("> "))

				if computer_prompt2 == 1:

					computer3 = True

					while computer3:

						print "\n1. A6-HJT3"
						print "2. C5-TZ"
						print "3. F3-763G"
						print "4. G1-GG"
						print "5. <- back"

						computer_prompt3 = int(raw_input("> "))

						if computer_prompt3 == 5:
							print "..."
							computer3 = False
						else:
							print "Nothing of interest here."

				elif computer_prompt2 == 2:

					computer4 = True

					while computer4:

						print "\n1. H5-I54"
						print "2. K5-22TS"
						print "3. L0-002"
						print "4. <- back"

						computer_prompt4 = int(raw_input("> "))

						if computer_prompt4 == 2:
							print "Yes that's the number Wanda was talking about."
							print "It says it's in the Warehouse on shelf T-1."
							score.calculate(the_player,'find motor')
							print "You log out of computer."
							computer5 = False
							computer4 = False
							computer3 = False
							computer2 = False
							computer = False

						elif computer_prompt4 == 4:
							print "..."
							computer4 = False
						else:
							print "Nothing of interest here."

				elif computer_prompt2 == 3:

					computer5 = True

					while computer5:

						print "\n1. N7-44F"
						print "2. T9-F"
						print "3. WK-991"
						print "4. <- back"

						computer_prompt5 = int(raw_input("> "))

						if computer_prompt5 == 4:
							print "..."
							computer5 = False
						else:
							print "Nothing of interest here."

				elif computer_prompt2 == 4:
					computer2 = False
					print "..."

				else:
					custom_error.errortype(3)

		elif computer_prompt == 2:
			print "\nSome accounting program opens but it's not"
			print "what you need so you close it."
			custom_error.errortype(4)
		elif computer_prompt == 3:
			print "\nYou see files on bunch of employees. Nothing of interest here."
			custom_error.errortype(4)
		elif computer_prompt == 0:
			print "You log out of computer."
			computer = False
			return 'Motor Shop'
		else:
			custom_error.errortype(3)

def enter(the_player):

	the_player.location = 'Motor Shop'
	the_player.directions = ['Curling Street', 'left door', 'right door']

	print "\nLocation:", the_player.location
	print "-" * 30

	if the_player.location in the_player.visited:
		print "You're back at the shop."


	else:
		the_player.visited.append(the_player.location)

		print "Thankfully the doors were not locked but"
		print "just in case you block them with a nearby"
		print "table."
		print "There's no light here so you turn on your"
		print "flashlight to look around."
		print "\nYou see mostly fishing stuff and some raided"
		print "supplies. There is a counter close to the wall"
		print "and two doors, one on the left and one on the right."

	while True:
		print "There is a counter in front of you and two doors,"
		print "one on the left and other on the right."

		action = prompt.standard(the_player)

		if action == "curling street" and 'motor' not in the_player.inventory.keys():
			print "\nYou still haven't found the motor."
			print "It's too risky to leave now and return later"
			print "because of the zombie herd outside."
		elif action == "curling street" and 'cart' not in the_player.inventory.keys():
			print "\nYou still need something to put the motor in. It is"
			print "too heavy to carry it in hands. The Junction if kind of"
			print "far too."
		elif action == "curling street" and 'cart' and 'motor' in the_player.inventory.keys():
			print "\nYou put the motor in the cart and head out of Motor shop to"
			print "meet Wanda at Junction."
			the_player.visited.append('got the motor')
			print "Thankfully the zombie herd is on the other"
			print "side of the street, on the spot where"
			print "Wanda taunted it. You don't see her"
			print "so you head out to Junction..."

			custom_error.errortype(4)
			
			if 'got the motor' and 'Wanda' in the_player.visited:
				print "Wanda: 'You made it! Great. I see you got pretty"
				print "creative with that cart.'"

			if 'boat key' in the_player.inventory.keys():
				print "Well, we have the key and the motor so let's"
				print "go to Harrington River, it's not far."
			else:
				print "We still need that boat key. It's in the"
			
				print "lobby of Old Building on March Street."
			return 'Junction'
		elif 'left' in action:
			return 'Warehouse'
		elif 'right' in action:
			return 'Maintenance room'
		elif 'counter' in action:
			print "There are some papers scattered around with"
			print "dried blood on them."
			print "You see a closed laptop."
		elif 'laptop' in action:
			print "You open the laptop and to your surprise"
			print "it powers up."
			laptop(the_player)
		else:
			custom_error.errortype(3)


