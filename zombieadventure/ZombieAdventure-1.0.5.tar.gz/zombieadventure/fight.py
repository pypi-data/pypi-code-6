import random
import copy
import prompt
import score
import custom_error
import death
import enemies

class Encounter(object):


	def __init__(self, the_player, enemy):
		self.the_player = the_player
		self.enemy = enemy

	
	def player_attack(self, the_player, the_enemy):

		weapon_stats = {
		'fists': random.randint(1,6),
		'gun': random.randint(30,35),
		'knife': random.randint(10,15),
		'baseball bat': random.randint(8,13) + random.randint(2,6),
		}

		weapons = self.player_weapon(the_player)
		bonus = self.attack_bonus(the_player)

		num_of_weapons = len(weapons)
		w_num = 1

		weapon_table = {}

		print "\nAvailable weapons:"
		while w_num <= num_of_weapons:
	
			for weapon in weapons:
				print str(w_num) + '.' ,weapon
				w_num = w_num + 1
				weapon_table[weapon] = w_num - 1

		selected_weapon = prompt.select_weapon()

		for key, item in weapon_table.items():
			if selected_weapon == item:
				attack_points = weapon_stats.get(key) * bonus
				use_weapon = key
			else:
				pass

		if 'knife' or 'baseball bat' in the_player.inventory.keys():
			for weapon, condition in the_player.inventory.items():

				if condition > 0 and condition <= 5:
					print_condition = "weak"
				elif condition > 5 and condition <= 15:
					print_condition = "OK"
				else:
					print_condition = "fine"
		else:
			pass

		chance_of_missing = random.randint(0,5)	

		if chance_of_missing == 0:
			randomize_attack = 0
		else:
			if use_weapon == 'gun':
				the_player.inventory['gun'] = the_player.inventory['gun'] - 1
				if the_player.inventory['gun'] <= 0:
					attack_points = 0
					print "You don't have enough bullets."
				else:
					pass
			elif use_weapon == 'knife':
				the_player.inventory['knife'] = the_player.inventory['knife'] - 1
				if the_player.inventory['knife'] <= 0:
					attack_points = 0
					print "Your knife is broken." 
			elif use_weapon == 'baseball bat':
				the_player.inventory['baseball bat'] = the_player.inventory['baseball bat'] - 1
				if the_player.inventory['baseball bat'] <= 0:
					attack_points = 0
					print "Your baseball bat is broken."
			else:
				pass

			randomize_attack = attack_points * random.uniform(0.0,1.0)
			the_enemy.enemy_hp = the_enemy.enemy_hp - randomize_attack

		if 'Wanda' in the_player.visited:
			wanda_attack = random.randint(10,12) * random.uniform(0.0,1.0)
			the_enemy.enemy_hp = the_enemy.enemy_hp - wanda_attack
		else:
			pass

		if randomize_attack <= 0:
			print "\nYou miss!"
		else:
			print "\nYou hit %s with %s for %.2f hitpoint damage." % (the_enemy.enemy_name, use_weapon, randomize_attack)
			if use_weapon == 'gun':
				print "%d bullets left.\n" % the_player.inventory['gun']
			elif use_weapon == 'knife' or use_weapon == 'baseball bat':
				print "%s looks %s.\n" % (use_weapon.capitalize(), print_condition)
			else:
				pass

		if 'Wanda' in the_player.visited:

			if wanda_attack <= 0:
				print "\nWanda misses!"
			else:
				print "\nWanda hits %s for %.2f hitpoints." % (the_enemy.enemy_name, wanda_attack)

		
		custom_error.errortype(4)

		if the_enemy.enemy_hp <= 0:
			enemy_alive = False
		else:
			enemy_alive = True

		return enemy_alive


	
	def enemy_attack(self, the_player, the_enemy):

		chance_of_missing = random.randint(0,5)
		chance_of_infection = random.randint(1,50)

		if chance_of_missing == 0:
			randomize_enemy_attack = 0
		else:
			randomize_enemy_attack = the_enemy.enemy_attack * random.uniform(0.0,1.0)
			the_player.hitpoints = the_player.hitpoints - randomize_enemy_attack
			if chance_of_infection == 50:
				death.type(7,the_player)
			else:
				pass

		if randomize_enemy_attack <= 0:
			print "\n%s misses!" % the_enemy.enemy_name
		else:
			print "\n%s hits you for %.2f. You have %.2f hitpoints left." % (the_enemy.enemy_name, randomize_enemy_attack, the_player.hitpoints)

		if the_player.hitpoints <= 0:
			death.type(6, the_player)
		else:
			pass


	
	def player_weapon(self, the_player):
		
		available_weapons = ['fists']
		weapons = ['gun', 'knife', 'baseball bat']

	
		for weapon in weapons:
			if weapon in the_player.inventory.keys():
				available_weapons.append(weapon)
			else:
				pass

		return available_weapons

	def attack_bonus(self, the_player):

		male = the_player.male
		age = the_player.age
		
		if male == True:
			if age < 4:
				bonus = 0.2
			elif age < 8:
				bonus = 0.6
			elif age < 12:
				bonus = 1.1
			elif age < 17:
				bonus = 1.6
			elif age < 26:
				bonus = 2.0
			elif age < 33:
				bonus = 2.3
			elif age < 48:
				bonus = 2.0
			elif age < 61:
				bonus = 1.1
			elif age < 72:
				bonus = 0.8
			else:
				bonus = 0.2
		else:
			if age < 4:
				bonus = 0.2
			elif age < 8:
				bonus = 0.6
			elif age < 12:
				bonus = 1.0
			elif age < 17:
				bonus = 1.4
			elif age < 26:
				bonus = 1.9
			elif age < 33:
				bonus = 1.9
			elif age < 48:
				bonus = 1.8
			elif age < 61:
				bonus = 1.0
			elif age < 72:
				bonus = 0.5
			else:
				bonus = 0.1

		return bonus

	
	def start(self, the_player):


		create_enemy = enemies.SpawnEnemy(the_player, self.enemy)

		if self.enemy == 'random':
			created_enemy = create_enemy.generate_random(the_player)
		else:
			created_enemy = create_enemy.generate(the_player, self.enemy)

		the_enemy = enemies.Enemy(*created_enemy)

		enemy_alive = True

			
		initialize_fight = random.randint(0,1)

		print "\n"
		print "-------------"
		print "--- FIGHT ---"
		print "-------------"
		print "Your enemy is %s.\n" % (the_enemy.enemy_name)

		if initialize_fight == 0:
			print "You are quicker than %s, you get to attack first!" % the_enemy.enemy_name
			fight_order = 'player first'
		else:
			print "%s strikes first!" % the_enemy.enemy_name
			fight_order = 'enemy first'


		while enemy_alive:

			if fight_order == 'player first':
				enemy_alive = self.player_attack(the_player, the_enemy)
				if enemy_alive == True:
					self.enemy_attack(the_player, the_enemy)
				else:
					break

			elif fight_order == 'enemy first':
				if enemy_alive == True:
					self.enemy_attack(the_player, the_enemy)
					enemy_alive = self.player_attack(the_player, the_enemy)
				else:
					break
			else:
				pass

		print "Congratulations you kill %s." % the_enemy.enemy_name
		score.calculate(the_player, the_enemy.enemy_name)

		if the_enemy.enemy_name not in the_player.killed.keys():
			the_player.killed[the_enemy.enemy_name] = 1
		else:
			the_player.killed[the_enemy.enemy_name] = the_player.killed[the_enemy.enemy_name] + 1




