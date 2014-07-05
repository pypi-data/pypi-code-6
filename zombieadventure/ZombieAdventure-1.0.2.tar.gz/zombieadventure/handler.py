# -*- coding: utf-8 -*-

import glob
import os.path
import time
import ast
import player
import game
import prompt
import custom_error


def save(the_player):
	save_file_name = str(the_player.name) + '.sav'
	save_file = open(save_file_name, 'w')
	save_file.truncate()
	save_file.write(str(the_player.name) + "\n")
	save_file.write(str(the_player.age) + "\n")
	save_file.write(str(the_player.male) + "\n")
	save_file.write(str(the_player.inventory) + "\n")
	save_file.write(str(the_player.max_hitpoints) + "\n")
	save_file.write(str(the_player.hitpoints) + "\n")
	save_file.write(str(the_player.location) + "\n")
	save_file.write(str(the_player.visited) + "\n")
	save_file.write(str(the_player.score) + "\n")
	save_file.write(str(the_player.directions) + "\n")
	save_file.write(str(the_player.killed) + "\n")
	save_file.close()
	print "Saved as %s file" % save_file_name

def load():
	print chr(27) + "[2J"
	print "-" * 80
	print "Load game"
	print "-" * 80
	print "These are your previously saved characters:\n"
	
	saved_games = glob.glob('*.sav')

	num_of_saved_games = len(saved_games)+1
	num = 1

	while num < num_of_saved_games:

		for save_game in saved_games:
			print str(num) + '.', save_game.strip(' .sav')
			num = num + 1
	
	while True:
		try:
			action = prompt.load_menu()
			load_file_name = saved_games[action - 1]

			load_file = open(str(load_file_name),'r')
			print "\n--- Your selected character ---"
			print "Name: ", load_file.readline().strip("\n")
			print "Age: ", load_file.readline().strip("\n"), "years"
			print "Is male?: ", load_file.readline().strip("\n")
			
			inv_read = ast.literal_eval(load_file.readline())

			print "Inventory:"
			for key, item in inv_read.items():
				if key == 'gun':
					print "- %s (%d bullets left)" % (key, item)
				elif key == 'knife' or key == 'baseball bat':
					if item > 0 and item <= 5:
						print_condition = "weak"
					elif item > 5 and item <= 15:
						print_condition = "OK"
					else:
						print_condition = "fine"
					print "- %s (%s)" % (key, print_condition)					
				elif item > 0:
					print "- %s (%d)" % (key, item)
				elif item <= 0:
					pass

			print_max_hp = float(load_file.readline().strip("\n"))
			print "Hitpoints: %.1f" % float(load_file.readline().strip("\n")),"/ %.1f" % print_max_hp, "HP"
			print "Location: ", load_file.readline().strip("\n")
			load_file.readline().strip("\n")
			print "Score: ", load_file.readline().strip("\n"), "points"
			load_file.readline().strip("\n")
			print "Save file:", load_file_name
			print "Last played on:", time.ctime(os.path.getmtime(load_file_name))

			choose_to_load = prompt.load_game()

			load_file.seek(0)

			load_player_name = load_file.readline().strip("\n")
			load_player_age = load_file.readline().strip("\n")
			load_player_male = load_file.readline().strip("\n")
			load_player_inventory = load_file.readline().strip("\n")
			load_player_max_hitpoints = load_file.readline().strip("\n")
			load_player_hitpoints = load_file.readline().strip("\n")
			load_player_location = load_file.readline().strip("\n")
			load_player_visited = load_file.readline().strip("\n")
			load_player_score = load_file.readline().strip("\n")
			load_player_directions = load_file.readline().strip("\n")
			load_player_killed = load_file.readline().strip()

			load_file.close()

			load_player_age = convert_save_file(load_player_age)
			load_player_max_hitpoints = convert_save_file(load_player_max_hitpoints)
			load_player_hitpoints = convert_save_file(load_player_hitpoints)
			load_player_male = convert_save_file(load_player_male)
			load_player_inventory = convert_save_file(load_player_inventory)
			load_player_visited = convert_save_file(load_player_visited)
			load_player_score = convert_save_file(load_player_score)
			load_player_directions = convert_save_file(load_player_directions)
			load_player_killed = convert_save_file(load_player_killed)

			if choose_to_load == "y":

				load_player = player.Player(load_player_name, 
									load_player_age, load_player_male, 
									load_player_inventory, load_player_max_hitpoints, 
									load_player_hitpoints, load_player_location, 
									load_player_visited, load_player_score, 
									load_player_directions, load_player_killed)

				load_game = game.Engine(load_player, load_player_location)
				load_game.move()

			elif choose_to_load == "n":
				load_file.close()
				load()

		except IndexError:
			print "This save game does not exit."


def convert_save_file(file_content):
	converted_content = ast.literal_eval(file_content)
	return converted_content
