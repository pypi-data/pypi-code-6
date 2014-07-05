import death
import apartment
import curling_street
import junction
import march_street
import twentysecond_street
import foreman_ave
import harrington_river
import marina
import old_building
import old_building_1f
import old_building_2f
import suburbs
import suburb_1
import suburb_2
import suburb_3
import suburb_4
import suburb_5
import suburb_6
import pirate_house
import basement
import kitchen
import suburb_junction
import cherry_tree
import small_houses
import very_long_street
import wandas_house
import motor_shop
import warehouse
import maintenance_room
import restroom
import wandas_boat
import ending

class Engine(object):

	def __init__(self, the_player, start_map):
		self.the_player = the_player
		self.start_map = start_map

		
	def move(self):
		
		if self.the_player.age >= 100:
			death.type(1)
		elif self.the_player.age <= 3:
			death.type(2)
		else:
			pass

		current_map = Maps.map_dict.get(self.start_map)
		
		while True:
			
			get_next_map = current_map.enter(self.the_player)
			current_map = Maps.map_dict.get(get_next_map)

			if get_next_map == None:
				pass
			else:
				pass


class Maps(object):

	map_dict = {
	'Apartment': apartment,
	'Curling Street': curling_street,
	'Junction': junction,
	'March Street': march_street,
	'22nd Street': twentysecond_street,
	'Foreman Ave': foreman_ave,
	'Harrington River': harrington_river,
	'Old Building': old_building,
	'Old Building (first floor)': old_building_1f,
	'Old Building (second floor)': old_building_2f,
	'Suburbs': suburbs,
	'Suburb 1': suburb_1,
	'Suburb 2': suburb_2,
	'Suburb 3': suburb_3,
	'Suburb 4': suburb_4,
	'Suburb 5': suburb_5,
	'Suburb 6': suburb_6,
	'Suburb Junction': suburb_junction,
	'Small houses': small_houses,
	'House with pirate flag': pirate_house,
	'Basement': basement,
	'Kitchen': kitchen,
	'Cherry trees': cherry_tree,
	'A very long street': very_long_street,
	'Wandas House': wandas_house,
	'Motor Shop': motor_shop,
	'Warehouse': warehouse,
	'Maintenance room': maintenance_room,
	'Restroom': restroom,
	'Marina': marina,
	'Wanda\'s boat': wandas_boat,
	'Ending': ending

	}

	def visited(self):
		visited_maps = map_dict.keys()


	

	





	
