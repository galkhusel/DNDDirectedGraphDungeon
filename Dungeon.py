import csv
import random
import datetime
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
	def __init__(self, name, data, power : int , max_power):
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

	def get_data(self):
		return self.data

	def get_power(self):
		return self.power

	def get_max_power(self):
		return self.max_power

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
	def get_origin(self):
		return self.origin
	def get_destination(self):
		return self.destination
	def get_data(self):
		return self.data
	def get_power(self):
		return self.power
	def get_max_power(self):
		return self.max_power

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


def build_dungeon(paths, locations, partys, mainp):


	position_dic = {}
	party_dic = {}
	main_party = None

	with open(paths) as path, open(locations) as location, open(partys) as party, open(mainp) as mp:
		paths = csv.reader(path)
		locations = csv.reader(location)
		partys = csv.reader(party)
		mparty = csv.reader(mp)

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
				int(x[2]) if int(x[2]) >= 1 else '1',
				x[3],
				x[4].strip()
				)

		main = next(mparty)

		main_party =  Party(
				main[0],
				main[1],
				int(main[2]) if int(main[2]) >= 1 else '1',
				main[3],
				main[4].strip()
				)



	return position_dic, party_dic, main_party


"""
====================================================================================================
====================================================================================================
								

								save instance functions

====================================================================================================					
====================================================================================================
"""

def writepath(path_object , path):

	path.writerow([
		path_object.get_name(),
		path_object.get_origin(),
		path_object.get_destination(),
		path_object.get_data(),
		path_object.get_power(),
		path_object.get_max_power(),
		])

def writelocation(location_object , location):
	location.writerow([
		location_object.get_name(),
		location_object.get_data(),
		location_object.get_power(),
		location_object.get_max_power(),
		])

def save_situation_position(position_dic, pathcsv, locationcsv, date):


	with open(pathcsv+date, 'w', newline='') as path, open(locationcsv + date, 'w', newline='') as location :

		paths = csv.writer(path)
		locations = csv.writer(location)


		for x in main_party:
			
			if x is int:
				writelocation(party_dic[x], locations)

			else:
				writepatj(party_dic[x], paths)

	return 1

def save_situation_main(main_party, maincsv, date):

	with open(maincsv+date, 'w', newline='') as mainparty:

		writer = csv.writer(mainparty)
		print(main_party)
		for x in main_party:
			
			row = [party_dic[x].get_name(),
				party_dic[x].get_description(),
				party_dic[x].get_power(),
				party_dic[x].get_location(),
				party_dic[x].get_adventurer()
				]
			writer.writerow(row)

	return 1

def save_situation_party(party_dic, partyscsv):

	with open(partyscsv+date, 'w', newline='') as party:

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

def save_situation(position_dic, party_dic, main_party, pathcsv, locationcsv, partyscsv, maincsv):
	date = datetime.datetime.now()
	save_situation_party(party_dic, partyscsv, date)
	save_situation_main(main_party, maincsv, date)
	save_situation_position(position_dic, pathcsv, locationcsv, date)

"""
====================================================================================================
====================================================================================================
								

								travelling in the dungeon functions

====================================================================================================					
====================================================================================================
"""

def adjust_power_level(positions, actual_position, party):
	return 

def make_connection_list(positions, actual_position):
	list_aux = list(positions[actual_position].get_connections())
	list_connections = []
	for x in list_aux:
		list_connections.append(positions[x].get_names_powers())
	return list_connections

def other_party_movement(positions, partys):

	for p_name in partys:
		actual_position = partys[p_name].get_location()
		list_connections = make_connection_list(positions, actual_position)
		partys[p_name].random_travel(list_connections)
		
		print(partys[p_name].get_name() + " is in " + partys[p_name].get_location())


	return 1

def main_party_travel(positions, main_party, travel):



		actual_position = main_party.get_location()
		lista = list(positions[actual_position].get_connections())

		if travel in lista:

			main_party.travel(positions[travel])
			positions[main_party.get_location()].show_info()

		else:
			print(travel + "not found")




		

def enter_dungeon(positions, partys, main_party):
		
	travel = 1

	positions[main_party.get_location()].show_info()


	while travel != "Quit":

		print("travel to where?")
		print("enter a path or Quit")
		travel = input()


		print("--------------------")
		print("--------------------")		
		print()
		print()
		print()
		print()
		other_party_movement(positions, partys)
		main_party_travel(positions, main_party, travel)






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

	print("saving progress")
	save_situation(position_dic, party_dic, main_party, "paths.csv", "locations.csv", "partys.csv", "mainParty.csv")

main()
