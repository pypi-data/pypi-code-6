# adventure game w/ 4 levels, 2 files
# based on LPTHW

from sys import exit
from random import randint
from time import sleep

class Cell:
	
	def __init__(self):
		self.dead = Dead('You die!')
		self.orc = Orc()

	print "*" * 40
	print "*" * 40
	print "*" * 8 + "ESCAPE FROM  THE DUNGEON" + "*" * 8
	print "*" * 40
	print "*" * 40
	print "You were captured during a battle."
	sleep(3)
	print "You awake in a small cell in a dungeon."
	sleep(3)
	print "You see light coming through a small hole."
	sleep(3)
	print "The wall is damaged..."

	def cell_intro(self):
	
		choice = raw_input("> Choose '1' to dig, '2' to do nothing: ")
	
		if choice == '1':
			chance = randint(0, 5)
			if chance != 3:
				print "You continue to dig through the hole."
				print "You make your way through a tunnel."
				return self.orc.orc_intro()
			else:
				print "Uh oh! The wall collapses!"
				return self.dead.death()
			
		elif choice == '2':
			print "Bad choice. You starve."
			return self.dead.death()
		
		else:
			print "You need to learn how to type!"
			return self.cell_intro()

live_score = [ ]

class Orc:
	
	def __init__(self):
		self.dead = Dead('You die! No big deal')
		self.snake = Snake()
		self.player_hp = 100
		self.orc_hp = 80
		self.player_moves = {'punch': 30, 'kick': 50, 'strangle': 70}
		self.orc_moves = {'slaps': 5, 'smashes': 7, 'clubs': 10}
		
	def orc_intro(self):
		print "*" * 40
		print "*" * 40
		print "*" * 12 + "LAIR OF  THE ORC" + "*" * 12
		print "*" * 40
		print "*" * 40
		print "You crawl out of the narrow tunnel and enter a large room."
		sleep(3)
		print "You are not alone. In one corner is a sleeping Orc."
		sleep(3)
		print "You see an open door on the other side of the room."
		sleep(3)
		print "Do you walk or run to the door?"
		
		choice = raw_input("> Choose '1' to walk and '2' to run: ")
		
		if choice == '1':
			
			chance = randint(0, 2)
			
			if chance == 1:
				print "You wake the Orc!"
				print "Looks like you need to fight him."
				return self.battle_turn()
			else:
				print "You make it to the other side of the room."
				print "You walk through the door..."
				return self.snake.snake_intro() 
		
		elif choice == '2':
			print "You wake the Orc!"
			print "Looks like you need to fight him."		
			return self.battle_turn()
	
		else:
			print "You need to learn to type! Next time you die!"
			return self.orc_intro()
	
	def battle_turn(self):
		
		chance = randint(0, 10)
		
		if chance <= 5:
			print "The Orc attacks first!"
			return self.orc_attack()
		else:
			print "You attack first!"
			return self.player_attack()
	
	def orc_attack(self):
		
		while self.orc_hp > 0:
			
			chance = randint(1, 5)
			if chance <= 3:
				orc_attack_choice = randint(1, 3)
				if orc_attack_choice == 1:
					print "The Orch slaps you!"
					self.player_hp -= self.orc_moves['slaps']
					print "You take %s points in damage." % self.orc_moves['slaps']
					print "You now have %s HPs." % self.player_hp
					if self.player_hp > 0:
						return self.player_attack()
					else:
						print "The Orc kills you!"
						return self.dead.death()
				
				elif orc_attack_choice == 2:
					print "The Orch smashes you!"
					self.player_hp -= self.orc_moves['smashes']
					print "You take %s points in damage." % self.orc_moves['smashes']
					print "You now have %s HPs." % self.player_hp
					if self.player_hp > 0:
						return self.player_attack()
					else:
						print "The Orc kills you!"
						return self.dead.death()
									
				else:
					print "The Orch clubs you!"
					self.player_hp -= self.orc_moves['clubs']
					print "You take %s points in damage." % self.orc_moves['clubs']
					print "You now have %s HPs." % self.player_hp
					if self.player_hp > 0:
						return self.player_attack()
					else:
						print "The Orc kills you!"
						return self.dead.death()		
					
			else:
				print "The Orc misses!"
				return self.player_attack()
				
	def player_attack(self):
	
		while self.player_hp > 0:
		
			print "Choose attack method."
			player_attack_choice = raw_input("> Choose 'punch', 'kick' or 'strangle' ")
			player_attack_choices = player_attack_choice.lower()
			
			if (player_attack_choices == 'punch' or player_attack_choices == 'strangle' or player_attack_choices == 'kick'):
			
				chance = randint(1, 2)
		
				if chance == 1:
					print "You %s the Orc!" % player_attack_choices
					self.orc_hp -= self.player_moves[player_attack_choices]	
					print "The Orc takes %s points in damage." % self.player_moves[player_attack_choices]
					print "The Orc now has %s HPs." % self.orc_hp
					if self.orc_hp > 0:
						return self.orc_attack()
					else:
						print "You kill the Orc!"
						points = randint(1, 5) * 10
						print "\a\a\aYou get %s points!" % points
						live_score.append(points)
						print "You now have %s points." % sum(live_score)
						return self.snake.snake_intro()
				else:
					print "You miss!"
					return self.orc_attack()
	
			else:
				print "Choose a listed option please."
				return self.player_attack()
	
class Snake:
	
	def __init__(self):
		self.dead = Dead("You've been ganked!")
		self.code_room = Code_Room()
		self.player_hp = 100
		self.snake_hp = 50
		self.player_moves = {'chop': 25, 'bite': 35}
		self.snake_moves = {'bite': 15, 'strangle': 20}
	
	def snake_intro(self):
		print "*" * 40
		print "*" * 40
		print "*" * 15 + "DOOR  ROOM" + "*" * 15
		print "*" * 40
		print "*" * 40
		print "The Orc is dead but you are far from out of the dungeon."
		sleep(3)
		print "You wipe yourself off and walk through the open door."
		sleep(3)
		print "You arrive in a room with two doors. A red one and a blue one."
		sleep(3)
		print "Which do you choose?"
		
		choice = raw_input("> Choose 'red' or 'blue'")
		door_choice = choice.lower()
		
		if (door_choice == 'red' or door_choice == 'blue'):
			if door_choice == 'red':
				print "Ooops!"
				print "Poison darts shoot out of the wall. In short, you die."
				return self.dead.death()
			else:
				print "Good job!"
				points = randint(2, 7) * 5
				print "\aYou get %s points!" % points
				live_score.append(points)
				print "You now have %s points." % sum(live_score)
				return self.snake_room()
		else:
			print "Choose a listed option please."
			return self.snake_intro()
				
	def snake_room(self):
		print "*" * 40
		print "*" * 40
		print "*" * 15 + "SNAKE ROOM" + "*" * 15
		print "*" * 40
		print "*" * 40
		print "You enter a dark and moist room."
		sleep(3)
		print "Out of nowhere a big snake attacks you."
		
		chance = randint(1, 5)
		
		if chance != 1:
			print "You are quick and dodge the snake attack!"
			points = randint(3, 6) * 7
			sleep(3)
			print "You get %s points!" % points
			live_score.append(points)
			print "You now have %s points." % sum(live_score)
			return self.player_attack()
		else:
			print "You are too slow. The snake bites you."
			print "You slowly die."
			return self.dead.death()
			
	def player_attack(self):
	
		while self.player_hp > 0:
	
			print "You counter attack!"
			player_attack_choice = randint(1,3)
			if player_attack_choice == 1:
				print "You 'chop' the snake!"
				self.snake_hp -= self.player_moves['chop']
				sleep(3)
				print "The snake takes %s points in damage!" % self.player_moves['chop']
				if self.snake_hp > 0:
					return self.snake_attack()
				else:
					print "You chop and kill the snake!"
					points = randint(7,20) * 3
					sleep(3)
					print "You get %s points." % points
					live_score.append(points)
					print "You now have %s points." % sum(live_score)
					return self.code_room.code_rm()
			
			elif player_attack_choice == 2:
				print "You 'bite' the snake!"
				self.snake_hp -= self.player_moves['bite']
				sleep(3)
				print "The snake takes %s points in damage!" % self.player_moves['bite']
				if self.snake_hp > 0:
					return self.snake_attack()
				else:
					print "You bite and kill the snake!"
					points = randint(2,15) * 2
					print "You get %s points." % points
					sleep(3)
					live_score.append(points)
					print "You now have %s points." % sum(live_score)
					return self.code_room.code_rm()
			
			else:
				print "You miss!"
				return self.snake_attack()
				
	def snake_attack(self):
	
		while self.snake_hp > 0:
			
			print "The snake attacks!"
			snake_attack_choice = randint(1, 3)
			if snake_attack_choice == 1:
				print "The snake bites you!"
				self.player_hp -= self.snake_moves['bite']
				sleep(3)
				print "You take %s points in damage!" % self.snake_moves['bite']
				if self.player_hp > 0:
					return self.player_attack()
				else:
					print "The snake's bite kills you."
					return self.dead.death()
			
			elif snake_attack_choice == 2:
				print "The snake strangles you!"
				self.player_hp -= self.snake_moves['strangle']
				sleep(3)
				print "You take %s points in damage!" % self.snake_moves['strangle']
				if self.player_hp > 0:
					return self.player_attack()
				else:
					print "The snake strangles you dead."
					return self.dead.death()
				
			else:
				print "The snake misses!"
				return self.player_attack()		

class Code_Room:
	
	def __init__(self):
		self.dead = Dead("So long")
		self.escape = Escape()
		
	def code_rm(self):
		print "*" * 40
		print "*" * 40
		print "*" * 15 + "CODE  ROOM" + "*" * 15
		print "*" * 40
		print "*" * 40
		print "\nYou enter a tunnel and walk to the end."
		print "The is a door with a small, circular window."
		sleep(3)
		print "This leads outside!"
		print "You see ten buttons with numbers 1 to 10 on the door."
		sleep(3)
		print "There is a parrot in a cage that keeps yapping.."
		print "YAAAAP! Enter the right number to exit! YAAP! 1 number, 3 tries! YAAP!"
		sleep(3)
		print "Better guess right or yee will die! YAAP!"
		
		right_guess = randint(1, 10)
		count = 0
	
		while count < 3:
		
			guess = raw_input("> Enter your guess ")
			guess_c = int(guess)	 
			 
			if guess_c == right_guess:
				print "Right guess is %s." % right_guess 		
				print "Right choice! The door opens and you escape the dungeon!"
				return self.escape.escape_intro()
			elif (guess_c != right_guess and count < 3):
				print "Right guess is %s." % right_guess
				print "Wrong guess."
				count += 1
				print "The count is now %s." % count
				left = 3 - count
				print "You have %s guesses left." % left
				if left == 0:
					print "You are out of guesses!"
					print "A trap door opens beneath you and you plummet to your death."
					return self.dead.death()
				else:
					pass			
			else:
				print "You are out of guesses!"
				print "A trap door opens beneath you and you plummet to your death."
				return self.dead.death()
		
class Escape:

	def escape_intro(self):
		print "*" * 40
		print "*" * 40
		print "*" * 16 + "YOU  WIN" + "*" * 16
		print "*" * 40
		print "*" * 40
		print "Good job! You win!"
		points = randint(10, 20) * 10
		print "You get %s points!" % points
		live_score.append(points) 
		print "Your final score is %s." % sum(live_score)	

class Dead:
	
	def __init__(self, why):
		self.why = why
		self.quips = ['Ha! ha! ha!',
			'Hardy har har',
			'So long, farewell',
			'Goodbye now'
			]
			
	def death(self):
		print self.why
		print self.quips[randint(0, 3)]
		exit(0)

game = Cell()
game.cell_intro()