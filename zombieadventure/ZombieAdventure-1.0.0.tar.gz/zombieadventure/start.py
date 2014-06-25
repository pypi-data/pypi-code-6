import sys
import custom_error
import player
import handler
import prompt
import splashscreen
import game
import death

def splash_screen():
	print chr(27) + "[2J"
	splashscreen.intro()
	print "*" * 80
	print "***** Welcome to ZOMBIE ADVENTURE ******"
	print "**  version 1 - Ondrej Synacek, 2014  **"
	print "*" * 80
	print "Select option:"
	print "1. Start a new game"
	print "2. Load existing game"
	print "3. Quit"

	while True:
		action = prompt.menu()

		if action == 1:
			create_player = player.CreateNewPlayer()
			create_player_args = create_player.generate()
			the_player = player.Player(*create_player_args)

			if the_player.male == True:
				gender = "man"
			else:
				gender = "woman"

			print "\nYour name is %s and you're %d old." % (the_player.name, the_player.age)
			print "You're a %s. Your maximum hitpoints are %.1f." % (gender, the_player.hitpoints)

			print "\n1. Continue to game"
			print "2. Back to main menu"
			action = prompt.menu()

			
			if action == 1:

				if the_player.age <= 3:
					death.type(2, the_player)
				elif the_player.age >= 141:
					death.type(1, the_player)
				else:
					pass
	

				print chr(27) + "[2J"

				splashscreen.new_game()
				custom_error.errortype(4)

				prompt.game_help()
				custom_error.errortype(4)
				
				a_game = game.Engine(the_player, 'Apartment')
				a_game.move()

			elif action == 2:
				handler.load()
			else:
				custom_error.errortype(3)
				custom_error.errortype(2)
				splash_screen()
				# a_game = game.Engine()
				# a_game.launch_game(the_player)
		elif action == 2:
			handler.load()
		elif action == 3:
			exit(1)
		else:
			custom_error.errortype(0)


splash_screen()

