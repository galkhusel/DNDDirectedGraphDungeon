import csv
import random

"""
====================================================================================================
====================================================================================================
								

										classes functions

====================================================================================================					
====================================================================================================
"""



#class Location would emulate Nodes in a Graph. 
#the power variable indicates if a party can enter the Location the power variable varies it goes from 0 to the original value + 3
# when an adventurer party enters Location the power value descends by the amount of the current power lvl of the adventurers 
# when a monster party enters a Location it may rise the power value of Location by up to 3 points of the original power 
class Location:
	# 	def __init__(self, name, data, power : int, max_power,  objectives , status):
	def __init__(self, name, data, power : int, max_power):
		self.name = name
		self.paths = {}
		self.data = data
		self.power = power
		self.original_power = power
		self.max_power = max_power

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


class Path:
	#	def __init__(self, origin, destination ,name, data, power : int, max_power, objectives, status):
	def __init__(self, origin, destination ,name, data, power : int, max_power):
		self.name = name
		self.origin = origin
		self.destination = destination
		self.data = data
		self.power = power
		self.original_power = power
		self.max_power = max_power

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
	#def __init__(self, name, description ,power : int, location, party_composition : {} , adventurer : bool, chase : bool):	
	def __init__(self, name, description ,power : int, location, adventurer : bool):
		self.name = name
		self.description = description
		self.power = power
		self.original_power = power
		self.location = location
		self.objectives = {}
		self.adventurer = adventurer
		self.paths = []


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

	def get_adventurer(self):
		return self.adventurer

	def travel(self, new_place):
		self.location = new_place.get_name()

	def random_travel(self, places):
        
		amount_places = len(places)

		new_place = random.choice(places)
		aux_places = 1

		while new_place[1] >> self.power and aux_places << amount_places:
			new_place = random.choice(places)
			aux_places += 1

		if aux_places << amount_places:
			self.location = new_place[0]

"""
====================================================================================================
====================================================================================================
								

								building dungeon functions


====================================================================================================					
====================================================================================================
"""


def build_dungeon(paths, locations, partys, main_party):


	position_dic = {}
	party_dic = {}
	main_party = None

	with open(paths) as path, open(locations) as location, open(partys) as party, open(main_party) as mp:
		paths = csv.reader(path)
		locations = csv.reader(location)
		partys = csv.reader(party)
		mpartys = csv.reader(mp)

		for x in locations:
			position_dic[x[0]] = Location(
				x[0],
				x[1],
				int(x[2]) if int(x[2]) >= 0 else 0,
				int(x[3]) if int(x[3]) >= 0 else int(x[2]) if int(x[2]) >= 0 else 0 
				)

		for x in paths:
			p = Path(
				x[0],
				x[1],
				x[2],
				x[3],
				int(x[4]) if int(x[4]) >= 0 else 0,
				int(x[5]) if int(x[5]) >= 0 else int(x[4]) if int(x[4]) >= 0 else 0
				)


			position_dic[p.name] = p
			position_dic[p.origin].add_path(p)


		for x in partys:
			
			#the strip is places in here to prevent save situation putting empty lines in the csv
			party_dic[x[0]] = Party(
				x[0],
				x[1],
				int(x[2]) if int(x[2]) >= 1 else '1s',
				x[3],
				x[4].strip()
				)
		for x in main_party:
			main_party =  Party(
				x[0],
				x[1],
				int(x[2]) if int(x[2]) >= 1 else '1s',
				x[3],
				x[4].strip()
				)



	return position_dic, party_dic, main_party


"""
====================================================================================================
====================================================================================================
								

								save instance functions

====================================================================================================					
====================================================================================================
"""

def save_situation(position_dic, party_dic, main_party, pathcsv, locationcsv, partyscsv, maincsv)

	save_situation_party(party_dic, partyscsv)

def save_situation_party(party_dic, partyscsv):
	with open(partyscsv, 'w', newline='') as party:

		writer = csv.writer(party)
		print(party_dic)
		for x in party_dic:
			
			row = [party_dic[x].get_name(),
				party_dic[x].get_description(),
				party_dic[x].get_power(),
				party_dic[x].get_location(),
				party_dic[x].get_adventurer()
				]
			writer.writerow(row)

	return 1

"""
====================================================================================================
====================================================================================================
								

								travelling in the dungeon functions

====================================================================================================					
====================================================================================================
"""

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

def main_party_travel(positions, partys, partys_names, main_party):
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

def enter_dungeon(positions, partys, partys_names, main_party):
		
		print("--------------------")
		print("--------------------")		
		print()
		print()
		print()
		print()

		other_party_movement(positions, partys, partys_names)

		if travel == "Quit":
			print("saving progress")



"""
====================================================================================================
====================================================================================================
								

											main

====================================================================================================					
====================================================================================================
"""

def main():




	position_dic, party_dic, main_party = build_dungeon("paths.csv", "locations.csv", "partys.csv", "mainParty.csv")

	enter_dungeon(position_dic, party_dic, main_party)

	save_situation(position_dic, party_dic, main_party, "paths.csv", "locations.csv", "partys.csv", "mainParty.csv")

main()
