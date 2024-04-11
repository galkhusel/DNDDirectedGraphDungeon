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
		self.deads = deads
		self.connection = {}

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
		if path in self.connection.values(): return path 

	def show_info(self):
		print("currently in Room: " + self.name)
		print("paths" + str(list(self.connection.keys())))
		print(self.data)
		print(self.deads)
		return 1
	
	def get_connections(self):
		return list(self.connection.keys())

class Path(Room):
	def __init__(self, name, data, deads, origin, destination):
		super().__init__(name, data, deads)
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
		print("origin : " + str(self.connection["origin"]) + " - destination : " + str(self.connection["destination"]))
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
	def __init__(self, name, health, max_health, cr, alive, heal_capacity, party, resting_place):
		super().__init__(name, alive)
		self.health = health
		self.max_health = max_health
		self.cr = cr
		self.heal_capacity = heal_capacity
		self.party = party
		self.resting_place = resting_place
		
	def killed(self, resting_place):
		self.resting_place = resting_place
		self.set_alive(False)

	def get_resting_place(self):
		return self.resting_place

	def get_heal_capacity(self):
		return self.heal_capacity
	
	def get_health(self):
		return self.health

	def set_health(self, value):
		self.health = value

	def get_party(self):
		return self.party

	def get_max_health(self):
		return self.max_health
	
	def get_cr(self):
		return self.cr

	def deal_damage(self, damage, resting_place):
		if self.get_alive():
			if self.health - damage <= 0:
				self.health = 0 
				self.killed(resting_place)
			else:
				self.health -= damage
	
	def self_heal(self):
		if self.health + self.heal_capacity <= self.max_health:
			self.health += self.heal_capacity
		else:
			self.set_health(self.max_health)

class Party(Entity):

	def __init__(self,name, description, room, side : bool, alive):
		super().__init__(name, alive)
		self.description = description		
		self.room = room
		self.side = side

		self.adventurers = {}

	def party_destroy(self, resting_place):
		deads = []
		for x in self.adventurers:
			self.adventurers[x].killed(resting_place)
			self.set_alive(False)
			deads.append(x)
		return deads

	def add_adventurer(self, adventurer):
		self.adventurers[adventurer.get_name()] = adventurer

	def remove_adventurer(self, adventurer):
		return self.adventurers.pop(adventurer.get_name())

	def show_info(self):
		print(self.name + self.description + self.room)
		return 1

	def get_room(self):
		return self.room

	def get_description(self):
		return self.description

	def get_side(self):
		return self.side

	def get_adventurers(self):
		return self.adventurers

	def get_specific_adventurer(self, adventurer):
		if adventurer in self.adventurers:	return self.adventurers[adventurer]
		return None
	
	def set_room(self, room: Room):
		self.room = room
	
	def set_side(self, side):
		self.side = side
	
	def travel(self, new_place):
		self.room = new_place
		return new_place

	def random_travel(self, Rooms):
		print("entre")
		print(Rooms)
		self.set_room(random.choice(Rooms))

	def calculate_damage(self):
		damage = 0
		for x in self.adventurers:
			damage += self.adventurers[x].get_cr()
		return damage
	
	def get_adventurers_alive(self):
		return [self.adventurers[x] for x in self.adventurers if self.adventurers[x].get_alive()] 

	def distribute_damage(self, damage, resting_place):
		alive = self.get_adventurers_alive()
		distributed_damage = damage // len(alive)
		dead = []
		for x in alive:
			x.deal_damage(distributed_damage)
			if not x.get_alive():
				dead.append(x.get_name())
		if len(dead) == len(alive):
			self.set_alive(False)
		return dead