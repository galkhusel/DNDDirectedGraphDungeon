import random

"""
====================================================================================================
====================================================================================================
								

										classes functions

====================================================================================================					
====================================================================================================
"""

class Location:
	# 	def __init__(objectives, status):
	def __init__(self, name, data ):
		self.name = name
		self.paths = {}
		self.data = data
		self.deads = []

	def add_path(self, path):
		self.paths[path.name] = path

	def get_connections(self):
		return self.paths.keys()

	def show_info(self):
		print("currently in Location: " + self.name)
		print("paths" + str(list(self.paths.keys())))
		print(self.data)


	def get_name(self):
		return self.name

	def get_data(self):
		return self.data

	def add_deads(self, dead):
		self.deads.append(dead)


class Path:
	#	def __init__(objectives, status):
	def __init__(self, origin, destination ,name, data):
		self.name = name
		self.origin = origin
		self.destination = destination
		self.data = data
		self.deads = []

	def get_connections(self):
		return [self.origin, self.destination]

	def get_name(self):
		return self.name

	def show_info(self):
		print("currently in path: " + self.name)
		print("origin : " + self.origin + " - destination : " + self.destination)
		print(self.data)
		print(self.deads)
		return 1

	def get_origin(self):
		return self.origin

	def get_destination(self):
		return self.destination

	def get_data(self):
		return self.data

	def add_deads(self, dead):
		self.deads.append(dead)


class Adventurers:
	def __init__(self, name, health, max_health,cr ,alive):
		self.name = name
		self.health = health
		self.max_health = max_health
		self.alive = alive
		self.cr = cr

	def get_name(self):
		return self.name

	def get_health(self):
		return self.health

	def get_max_health(self):
		return self.max_health

	def get_alive(self):
		return self.alive
	
	def get_cr(self):
		return self.cr

	def set_name(self, name):
		self.name = name

	def set_health(self, health):
		self.health = health

	def set_status(self, status):
		self.status = status

	def calculate_damage(self, damage):
		if self.get_alive():
			self.health -= damage 
			if self.health <= 0:
				self.alive = False

class Party:
	#status indicate which party member are alive and their conditions, also the party inventory its a dic
	#def __init__(, objectives, chase, graph, status):	
	def __init__(self, name, description, location, side : bool, alive):
		self.name = name
		self.description = description
		self.location = location
		self.side = side
		self.alive = alive
		self.adventurers = {}

	def add_adventurer(self, adventurer):
		self.adventurers[adventurer.get_name()] = adventurer
		
	def show_info(self):
		print(self.name + self.description + self.location)
		return 1

	def get_location(self):
		return self.location

	def get_name(self):
		return self.name

	def get_description(self):
		return self.description

	def get_side(self):
		return self.side

	def get_alive(self):
		return self.alive

	def set_alive(self, alive):
		self.alive = alive

	def get_adventurers(self):
		return self.adventurers

	def set_location(self, location):
		self.location = location
	
	"""de aca para abajo hay que chequear"""
	def select_character_random(self):

		character_selection = random.choice(list(self.adventurers.keys()))
		character = self.adventurers[character_selection]

		picked_characters = [character_selection]

		amount_characters = len(self.adventurers)
		aux_amount_characters = 0

		while character.get_alive() == False and aux_amount_characters < amount_characters:

			character_selection = random.choice(list(self.adventurers.keys()))
			character = self.adventurers[character_selection]

			if character_selection not in picked_characters:

				picked_characters.append(character_selection)
				aux_amount_characters += 1

		if character.get_alive() == True:
			return character

		return None

	def status(self):
		
		print("the party is alive {}".format(self.alive))

		print("the party has {}".format(self.adventurers))

		return 1

	def set_side(self, side):
		self.side = side

	def travel(self, new_place):
		self.location = new_place.get_name()
		return new_place

	def random_travel_path(self, locations):
		print("entre path")
		self.set_location(random.choice(locations))
		return 
	
	def random_travel_location(self, locations):
		print("entre location")
		self.set_location(random.choice(locations))
		return 1

	def random_travel(self, places):
		print("entre")
		print(places)
		if self.location.isdigit():
		
			self.random_travel_location(places)

		else:

			self.random_travel_path(places)
		