import csv
import random

"""
--------------------------------------------------------------------------------------------------------------

Todo: 
	in Path and Location change data to a list or dictionary to save changes made by another party
	in Path and Location add things that can be harvested by npc to make items
	in Party add a action variable about what can be done by them when they enter a path or a location could be harves , consume items , stash items , secure the place . etc
	in party add a health or power meter that can changed based on what happens when someone enters a location or path they can die.
	in party add a list of places that the have been through.
	in party add a chaser property so the partys can chase each other.

--------------------------------------------------------------------------------------------------------------
"""

#class Location would emulate Nodes in a Graph. the power variable indicates if a party can enter the Location
class Location:
	# esta compuesto por una lista de vertices y la recorre de forma secuencial

	def __init__(self, name, data, power, objectives, rest):
		self.name = name
		self.paths = {}
		self.data = data
		self.power = power
		self.objectives = objectives

	def add_path(self, path):
		self.paths[path.name] = path

	def get_connections(self):
		return self.paths.keys()

	def show_info(self):
		print("currently in Location: " + self.name)
		print("paths" + str(list(self.paths.keys())))
		print(self.data)
		return 1

	def get_name(self):
		return self.name



class Path:
	def __init__(self, origin, destination ,name, data, power, objectives, rest):
		self.name = name
		self.origin = origin
		self.destination = destination
		self.data = data
		self.power = power
		self.objectives = objectives


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

class Party:
	def __init__(self, name, description, power, location, searching objectives, rest):
		self.name = name
		self.description = description
		self.power = power
		self.location = location

	def show_info(self):
		print(self.name + self.description + self.location)
		return 1

	def get_location(self):
		return self.location

	def get_name(self):
		return self.name

	def get_power(self):
		return self.power

	def get_description(self):
		return self.description

	def travel(self, new_place):
		self.location = new_place.get_name()

	def random_travel(self, places):

		new_place = random.choice(places)

		while new_place[1] >> self.power:
			new_place = random.choice(places)

		self.location = new_place[0]

def make_connection_list(positions, actual_position):
	list_aux = list(positions[actual_position].get_connections())
	list_connections = []
	for x in list_aux:
		list_connections.append(positions[x].get_names_powers())
	return list_connections

def other_party_movement(positions, partys, partys_names):

	for p_name in partys_names:
		actual_position = partys[p_name].get_location()
		list_connections = make_connection_list(positions, actual_position)
		partys[p_name].random_travel(list_connections)
		
		print(partys[p_name].get_name() + " is in " + partys[p_name].get_location())
	return 1

def save_situation(party_dic):
	with open("partys.csv", 'w', newline='') as party:

		writer = csv.writer(party)
		print(party_dic)
		for x in party_dic:
			
			row = [party_dic[x].get_name(),
				party_dic[x].get_description(),
				party_dic[x].get_power(),
				party_dic[x].get_location()]

			writer.writerow(row)


	return 1

def enter_dungeon(positions, partys, partys_names, main_party):

	travel = 1

	while travel != "Quit":

		actual_position = partys[main_party].get_location()
		lista = list(positions[actual_position].get_connections())

		positions[actual_position].show_info()
		print("travel to where?")

		travel = input()

		if travel not in lista and travel != "Quit" :
			print(travel + "not found")
			continue 

		if travel == "Quit":
			print("saving progress")
			continue

		partys[main_party].travel(positions[travel])

		other_party_movement(positions, partys, partys_names)
		print("--------------------")
		print("--------------------")		
		print()
		print()
		print()
		print()

		if travel == "Quit":
			print("saving progress")




def main():

	position_dic = {}
	party_dic = {}
	partys_names = []

	with open("paths.csv") as path, open("locations.csv") as location, open("partys.csv") as party:
		paths = csv.reader(path)
		locations = csv.reader(location)
		partys = csv.reader(party)

		for x in locations:
			position_dic[x[0]] = Location( x[0],x[1], int(x[2]) if int(x[2]) >= 0 else '0')

		for x in paths:
			p = Path(x[0], x[1], x[2], x[3], int(x[4]) if int(x[4]) >= 0 else '0')
			position_dic[p.name] = p
			position_dic[p.origin].add_path(p)


		for x in partys:
<<<<<<< HEAD:Dungeon.py
<<<<<<< Updated upstream:objetos.py
			party_dic[x[0]] = Party(x[0], x[1], int(x[2]) if int(x[2]) >= 1 else '1s', x[3])
=======
			#the strip is places in here to prevent save situation putting empty lines in the csv
			party_dic[x[0]] = Party(x[0], x[1], int(x[2]) if int(x[2]) >= 1 else '1s', x[3].strip())
>>>>>>> Stashed changes:Dungeon.py
=======
			party_dic[x[0]] = Party(x[0], x[1], int(x[2]) if int(x[2]) >= 1 else '1s', x[3].strip())
>>>>>>> 8d98fd4c74b6679b4b7eb6d5960ff1c5e56daa95:objetos.py
			partys_names.append(x[0])



	enter_dungeon(position_dic, party_dic, partys_names[1:],partys_names[0])
	save_situation(party_dic)

main()
