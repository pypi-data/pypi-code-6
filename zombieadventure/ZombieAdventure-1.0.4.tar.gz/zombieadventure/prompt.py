import random
import handler
import sys
import hint
import custom_error
import score
import death

def standard(the_player):

	push_ups = 1

	while True:
		
		user_input = str(raw_input("> ")).lower()		

		if user_input == "save":
			handler.save(the_player)
		elif user_input == "inventory" or user_input == "inv":
			print "Inventory:"
			for key, item in the_player.inventory.items():
				condition = item

				if condition > 0 and condition <= 5:
					print_condition = "weak"
				elif condition > 5 and condition <= 15:
					print_condition = "OK"
				else:
					print_condition = "fine"
				
				if key == 'knife' or key == 'baseball bat':					
					print "- %s (%s)" % (key, print_condition)
				elif key == 'gun':
					print "- %s (%d bullets left)" % (key, item)
				elif item > 0:
					print "- %s (%d)" % (key, item)
				elif item <= 0:
					pass

		elif user_input == "char":
			print "\n---", the_player.name, "---"
			print "Age:", the_player.age
			print "Is male?:", the_player.male
			print "Hitpoints: %.1f" % the_player.hitpoints, "/ %.1f" % the_player.max_hitpoints 
			print "Current location:", the_player.location
			print "Score:", the_player.score, "points","\n"
		elif user_input == "help":
			game_help()
		elif user_input == "look":
			print "You can go to:", ", ".join(the_player.directions)
		elif user_input == "hint":
			print "Hint:", hint.location(the_player.location)
		# EASTER EGG
		elif user_input == "push up" and the_player.age > 90:
			death.type(4, the_player)
		elif user_input == "push up" and push_ups > 18:
			death.type(5, the_player)
		elif user_input == "push up":
			push_up = score.calculate(the_player, 'push up')
			print "You've done %d sets of push ups." % push_ups
			push_ups = push_ups + 1
		elif user_input == "heal":
			if 'bandage' not in the_player.inventory.keys() or the_player.inventory['bandage'] == 0:
				print "You do not have bandage."

			elif the_player.hitpoints >= the_player.max_hitpoints:
				print "You don't need to heal yourself."

			elif the_player.inventory['bandage'] > 0:
				healed_hp = random.uniform(11.0,15.0)
				the_player.hitpoints = the_player.hitpoints + healed_hp
				the_player.inventory['bandage'] = the_player.inventory['bandage'] - 1

				if the_player.hitpoints > the_player.max_hitpoints:
					over_hp = the_player.hitpoints - the_player.max_hitpoints
					the_player.hitpoints = the_player.max_hitpoints
					healed_hp = healed_hp - over_hp
				else:
					pass

				print "\nYou heal %.1f hitpoints. (Now: %.1f/%.1f HP). %d bandages left." % (healed_hp, the_player.hitpoints, the_player.max_hitpoints, the_player.inventory['bandage'])
			else:
				pass
		elif user_input == "map":
			if 'map' in the_player.inventory.keys():
				print """
				WELTON SUBURBS MAP

 Left____Another St.____Longer St.____Row of H.
   |                                     |
Suburbs...Very long st.____Small h.___Junction____Mansion
   |                                     |
 Right____Regular St.____Shorter St.____St. w/ tree
"""				

			else:
				print "You don't have a map."
		elif user_input == "visited":
			print the_player.visited
		elif user_input == "killed":
			print the_player.killed
		elif user_input == "quit":

			print "Are you sure? Y/N"

			while True:
				to_quit = str(raw_input("> ")).lower()

				if to_quit == "y":
					break
				elif to_quit == "n":
					return ''
				else:
					custom_error.errortype(5)

			print "Do you want to save? Y/N"
				
			while True:
				save_input = str(raw_input("> ")).lower()

				if save_input == "y":
					handler.save(the_player)
					break
				elif save_input == "n":
					break
				else:
					custom_error.errortype(5)
			exit(1)
		else:
			return user_input


def menu():

	while True:
		try:
			user_input = int(raw_input("\nType a number > "))
			return user_input
		except ValueError:
			custom_error.errortype(1)
			

def load_menu():

		while True:
			try:
				user_input = int(raw_input("\nType a number or type 0 to QUIT > "))

				if user_input == 0:
					exit(1)
				else:
					return user_input
			except ValueError:
				custom_error.errortype(1)


def load_game():

	while True:
		try:
			user_input = str(raw_input("\nLoad this character? Y/N > ")).lower()

			if user_input == "y" or user_input == "n":
				return user_input
			else:
				custom_error.errortype(5)
		except ValueError:
			custom_error.errortype(3)

def select_weapon():

	while True:
		try:
			user_input = int(raw_input("\nSelect weapon (number) > "))
			return user_input
		except ValueError:
			custom_error.errortype(1)
		except IndexError:
			return None


def conversation():

	while True:
		try:
			user_input = int(raw_input("\nSelect answer (number) > "))
			return user_input
		except ValueError:
			custom_error.errortype(1)




def game_help():

	print "\n"
	print "-" * 80
	print "Type HELP anytime to display this message."
	print "-" * 80
	print "Type these commands anytime to perform actions:"
	print " * LOOK: See where you can go."
	print " * HINT: If you're stuck, you can get little help."
	print " * SAVE: Save your progress."
	print " * INV: Will display contents of your inventory."
	print " * CHAR: Shows character stats."
	print " * HEAL: Will heal your char if you have bandage(s)."
	print " * QUIT: Quit game."
	print "\n *** Don't use verbs with things, just nouns. ***\n"


