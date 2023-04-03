import random

"""
====================================================================================================
====================================================================================================
								

										classes functions

====================================================================================================					
====================================================================================================
"""

class Location:
	# status indicates the condition of the path depending on the power of the path its a dic
	# 	def __init__(objectives, status):
	def __init__(self, name, data, power : int, max_power ):
		self.name = name
		self.paths = {}
		self.data = data
		self.power = power
		self.original_power = power
		self.max_power = max_power
		#self.objectives = objectives
		self.status = {}

	def add_path(self, path):
		self.paths[path.name] = path

	def get_connections(self):
		return self.paths.keys()

	def show_info(self):
		print("currently in Location: " + self.name)
		print("paths" + str(list(self.paths.keys())))
		print(self.data)
		return 1

	def get_names_powers(self):
		return [self.name, self.power]

	def get_name(self):
		return self.name

	def get_data(self):
		return self.data

	def get_power(self):
		return self.power

	def set_power(self,boolean, power):
		if boolean != None:
			if boolean:
				self.power -= power
			if not boolean:
				self.power += power

	def get_max_power(self):
		return self.max_power

	def add_deads(self, deads):

		print(self.status)
		if "deads" not in self.status:
			self.status["deads"] = deads
		else:
			for x in deads:
				self.status["deads"].append(x)
	def get_status(self):
		return self.status
	def set_status(self, statusl):
		if self.status == {}:
			self.status = statusl
		else:
			for x in statusl:
				self.status[x] = statusl[x] 

class Path:
	#status indicates the condition of the path depending on the power of the path its a dic
	#	def __init__(objectives, status):
	def __init__(self, origin, destination ,name, data, power : int, max_power : int ):
		self.name = name
		self.origin = origin
		self.destination = destination
		self.data = data
		self.power = power
		self.max_power = max_power
		self.status = {}

	def get_connections(self):
		return [self.origin, self.destination]

	def get_name(self):
		return self.name

	def show_info(self):
		print("currently in path: " + self.name)
		print("origin : " + self.origin + " - destination : " + self.destination)
		print(self.data)
		return 1

	def get_names_powers(self):
		return [self.name, self.power]

	def get_origin(self):
		return self.origin

	def get_destination(self):
		return self.destination

	def get_data(self):
		return self.data

	def get_power(self):
		return self.power

	def set_power(self, boolean, power):
		if boolean != None:
			if boolean:
				self.power -= power
			if not boolean:
				self.power += power

	def get_max_power(self):
		return self.max_power

	def add_deads(self, deads):
		print(self.status)
		if "deads" not in self.status:
			self.status["deads"] = deads
		else:
			for x in deads:
				self.status["deads"].append(x)

	def get_status(self):
		return self.status

	def set_status(self, statusl):
		if self.status == {}:
			self.status = statusl
		else:
			for x in statusl:
				self.status[x] = statusl[x] 


class Adventurers:
	def __init__(self, name, health, max_health,  status, alive):
		self.name = name
		self.health = health
		self.max_health = max_health
		self.status = status
		self.alive = alive

	def get_name(self):
		return self.name

	def get_health(self):
		return self.health

	def get_status(self):
		return self.status

	def get_max_health(self):
		return self.max_health

	def get_alive(self):
		return self.alive

	def set_name(self, name):
		self.name = name

	def set_health(self, health):
		self.health = health

	def set_status(self, status):
		self.status = status

	def calculate_damage(self, damage):
		if self.get_alive():
			self.health += damage 
			if self.health <= 0:
				self.alive = False

class Party:
	#status indicate which party member are alive and their conditions, also the party inventory its a dic
	#def __init__(, objectives, chase, graph, status):	
	def __init__(self, name, description ,power : int, max_power:int , location, side : bool, alive):
		self.name = name
		self.description = description
		self.power = power
		self.max_power = max_power
		self.location = location
		self.side = side
		self.alive = alive

		self.adventurers = {}

		self.objectives = {}
		self.paths = []

	def add_adventurer(self, adventurer):
		self.adventurers[adventurer.get_name()] = adventurer
		
	def show_info(self):
		print(self.name + self.description + self.location)
		return 1

	def get_location(self):
		return self.location

	def get_name(self):
		return self.name

	def get_power(self):
		return self.power

	def get_max_power(self):
		return self.max_power

	def get_description(self):
		return self.description

	def get_side(self):
		return self.side

	def set_side(self):
		self.side = side


	def get_alive(self):
		return self.alive

	def set_alive(self, alive):
		self.alive = alive

	def get_adventurers(self):
		return self.adventurers

	def set_location(self, location):
		self.location = location
	
	def select_character(self):

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
			
		dead = None

		if self.power <= -1:

			character = self.select_character()

			if character != None:
				character.calculate_damage(self.power)
			
				if character.get_alive() == False:
					dead = character
					self.power = self.max_power

				else:
					self.power = 0

		return dead 

	def set_power(self, power):
		
		self.power = power
		deads = self.status()

		adventurers_alive = False

		for x in self.adventurers:
			if self.adventurers[x].get_alive():
				adventurers_alive = True
				break

		if adventurers_alive == False:
			self.alive = False
		return deads

	def set_side(self, side):
		self.side = side

	def travel(self, new_place):
		self.location = new_place.get_name()
		return new_place

	def random_travel_path(self, locations):

		if locations[1][1] <= self.power:
			self.power -= 1
			self.location = locations[1][0]

		elif locations[0][1] <= self.power and self.power == self.max_power:
			self.power -= 1
			self.location = locations[0][0]

		else :
			self.power += 1

	def obtain_travel(self, paths):

		amount_places = len(paths)
		new_place = random.choice(paths)
		aux_places = 0
		
		already_tried = []

		while new_place[1] > self.power:
			if aux_places == amount_places:break
			new_place = random.choice(paths)
			paths.remove(new_place)
			already_tried.append(new_place)

			aux_places += 1
			

		if aux_places <= amount_places and new_place[1] <= self.power:
			return new_place

		return None

	def random_travel_location(self, paths):

		new_location = self.obtain_travel(paths)

		if new_location != None:
			self.location = new_location[0]
			self.power -= 1

		elif self.power << self.max_power:

			self.power += 1

	def random_travel(self, places):
		
		if self.location.isdigit():

			self.random_travel_location(places)

		else:

			self.random_travel_path(places)