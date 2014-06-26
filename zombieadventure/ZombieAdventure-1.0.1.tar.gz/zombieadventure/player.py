import random
import sys
import copy
import glob
import os.path
import custom_error
import prompt
import game

class Player(object):

	def __init__(self, name, age, male,
				inventory, max_hitpoints, hitpoints, 
				location, visited, score, directions,
				killed):

		self.name = name
		self.age = age
		self.male = male
		self.inventory = inventory
		self.max_hitpoints = max_hitpoints
		self.hitpoints = hitpoints
		self.location = location
		self.visited = visited
		self.score = score
		self.directions = directions
		self.killed = killed
	
class CreateNewPlayer(object):

	def generate(self):
		print chr(27) + "[2J"
		print "-" * 80
		print "Character creation"
		print "-" * 80


		try:
			check_name = self.check_for_name(str(raw_input("Type down your name > ")))
		except ValueError:
			custom_error.errortype(3)
			self.generate()

		name = copy.deepcopy(check_name)

		try:
			age = int(raw_input("Put down your age in numbers > "))
		except ValueError:
			custom_error.errortype(1)
			custom_error.errortype(2)
			self.generate()


		if age <= 0:
			print "Number must be larger than zero."
			custom_error.errortype(2)
			self.generate()
		else:
			pass

		male = True
		sex = str(raw_input("Are you a male or female? M/F > ")).lower()

		if sex == "m":
			male = True
		elif sex == "f":
			male = False
		else:
			print "Please type either 'M' or 'F'"
			custom_error.errortype(2)
			self.generate()

		if male:
			male_hp_bonus = 1.6
			
			if age < 3:
				hitpoints = random.randint(1,3) * male_hp_bonus
			elif age < 5:
				hitpoints = random.randint(8, 10) * male_hp_bonus
			elif age < 12:
				hitpoints = random.randint(10, 13) * male_hp_bonus
			elif age < 17:
				hitpoints = random.randint(16, 22) * male_hp_bonus
			elif age < 26:
				hitpoints = random.randint(25,32) * male_hp_bonus
			elif age < 33:
				hitpoints = random.randint(25,30) * male_hp_bonus
			elif age < 48:
				hitpoints = random.randint(27,29) * male_hp_bonus
			else:
				hitpoints = random.randint(16,22) * male_hp_bonus
		
		else:
			female_hp_bonus = 1.2


			if age < 3:
				hitpoints = random.randint(1,3) * female_hp_bonus
			elif age < 5:
				hitpoints = random.randint(8, 10) * female_hp_bonus
			elif age < 12:
				hitpoints = random.randint(10, 13) * female_hp_bonus
			elif age < 17:
				hitpoints = random.randint(16, 22) * female_hp_bonus
			elif age < 26:
				hitpoints = random.randint(25,32) * female_hp_bonus
			elif age < 33:
				hitpoints = random.randint(25,30) * female_hp_bonus
			elif age < 48:
				hitpoints = random.randint(27,29) * female_hp_bonus
			else:
				hitpoints = random.randint(16,22) * female_hp_bonus

		
		max_hitpoints = copy.deepcopy(hitpoints)
			

		return name, age, male, {}, max_hitpoints, hitpoints, 'apartment', [], 0, [], {}

	def check_for_name(self, name):

		saved_games = glob.glob('*.sav')

		save_file = [name + '.sav']

		if save_file[0] in saved_games:
			custom_error.errortype(6)
			custom_error.errortype(2)
			self.generate()
		else:
			return name


