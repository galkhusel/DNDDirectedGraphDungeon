import random

"""
====================================================================================================
====================================================================================================
								

										classes functions

====================================================================================================					
====================================================================================================
"""
# añadir clase Room ocmo padre y tener como hijos camino(path) y room aplicar poly


class Room:
	def __init__(self, name, data, deads = []):
		self.name = name
		self.data = data
		self.connection = {}
		self.deads = deads

	def get_name(self):
		return self.name

	def get_data(self):
		return self.data

	def add_deads(self, dead):
		self.deads.append(dead)
	
	def get_deads(self):
		return self.deads

	def add_path(self, path):
		self.connection[path.name] = path

	def get_path(self, path):
		if path in self.connection:	return self.connection[path] 

	def show_info(self):
		print("currently in Room: " + self.name)
		print("paths" + str(list(self.connection.keys())))
		print(self.data)
		print(self.deads)
		return 1
	
	def get_connections(self):
		return list(self.connection.keys())

class Path(Room):
	def __init__(self, name, origin, destination, data):
		super().__init__(name, data)
		self.connection["origin"] = origin
		self.connection["destination"] = destination

	def get_connections(self):
		return [self.connection["origin"], self.connection["destination"]]

	def get_origin(self):
		return self.connection["origin"]

	def get_destination(self):
		return self.connection["destination"]
	
	def show_info(self):
		print("currently in path: " + self.name)
		print("origin : " + self.connection["origin"] + " - destination : " + self.connection["destination"])
		print(self.data)
		print(self.deads)
		return 1


class Entity:
	def __init__(self, name, alive):
		self.name = name
		self.alive = alive

	def get_name(self):
		return self.name
	
	def get_alive(self):
		return self.alive

	def set_alive(self, alive):
		self.alive = alive

class Adventurers(Entity):
	def __init__(self, name, health, max_health, cr, alive, heal_capacity):
		super().__init__(name, alive)
		self.health = health
		self.max_health = max_health
		self.cr = cr
		self.heal_capacity = heal_capacity

	def get_health(self):
		return self.health

	def set_health(self, value):
		self.health = value


	def get_max_health(self):
		return self.max_health
	
	def get_cr(self):
		return self.cr

	def deal_damage(self, damage):
		if self.get_alive():
			if self.health - damage <= 0:
				self.health = 0 
				self.set_alive(False)
			else:
				self.health -= damage
	
	def self_heal(self):
		if self.health + self.heal_capacity <= self.max_health:
			self.health += self.heal_capacity
		else:
			self.set_health(self.max_health)



class Party(Entity):

	def __init__(self,name, description, Room, side : bool, alive):
		super().__init__(name, alive)
		self.description = description		
		self.Room = Room
		self.side = side
		self.adventurers = {}


	def add_adventurer(self, adventurer):
		self.adventurers[adventurer.get_name()] = adventurer
		
	def show_info(self):
		print(self.name + self.description + self.Room)
		return 1

	def get_room(self):
		return self.Room

	def get_description(self):
		return self.description

	def get_side(self):
		return self.side

	def get_adventurers(self):
		return self.adventurers

	def get_specific_adventurer(self, adventurer):
		if adventurer in self.adventurers:	return self.adventurers[adventurer]
		return None
	
	def set_room(self, Room):
		self.Room = Room
	
	def set_side(self, side):
		self.side = side
	
	def select_character_random(self):

		alive_characters = [x for x in self.adventurers.keys() if self.adventurers[x].get_alive() == True]

		if len(alive_characters) == 0:
			return None
		character = random.choice(list(self.get_adventurers.keys()))
		return self.get_adventurers(character)

	def status(self):
		print("the party is alive {}".format(self.alive))
		print("the party has {}".format(self.adventurers))
		return 1

	def travel(self, new_place):
		self.Room = new_place.get_name()
		return new_place
	
	def random_travel(self, Rooms):
		print("entre")
		print(Rooms)
		self.set_room(random.choice(Rooms))
		