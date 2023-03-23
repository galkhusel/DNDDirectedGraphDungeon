import csv

class Location:
<<<<<<< Updated upstream:objetos.py
	# esta compuesto por una lista de vertices y la recorre de forma secuencial
	def __init__(self, name, data, power):
=======
	def __init__(self, name, data, power, objectives, rest):
>>>>>>> Stashed changes:Dungeon.py
		self.name = name
		self.paths = {}
		self.data = data
		self.power = power
		self.keys = keys

	def add_path(self, path):
		self.paths[path.name] = path

	def get_connections(self):
		return self.paths.keys()

	def show_info(self):
		print("paths" + str(list(self.paths.keys())))
		print(self.data)
		return 1

	def get_name(self):
		return self.name

class Path:
<<<<<<< Updated upstream:objetos.py

	def __init__(self, origin, destination ,name, data, power):
=======
	def __init__(self, origin, destination ,name, data, power, objectives, rest):
>>>>>>> Stashed changes:Dungeon.py
		self.name = name
		self.origin = origin
		self.destination = destination
		self.data = data
		self.power = power
		self.keys = keys


	def show_info(self):
		print("origin : " + self.origin + " - destination : " + self.destination)
		print(self.data)
		return 1

	def get_connections(self):
		return [self.origin, self.destination]

	def get_name(self):
		return self.name

class Party:
	def __init__(self, name, description, power, location, searching objectives, rest):
		self.name = name
		self.description = description
		self.power = power
		self.location = location

	def show_info(self):
		print(self.name + self.description + self.location)
		return 1

	def travel(self, new_place):
		self.location = new_place.get_name()

	def random_travel(self, places):

		new_place = random.choice(places)

		while new_place[1] >> self.power:
			new_place = random.choice(places)

		self.location = new_place[0]

	def get_location(self):
		return self.location


def enter_dungeon(positions, partys, partys_names):

	travel = 1

	main_party = partys_names[0]
	while travel != "Quit":

		position = partys[main_party].get_location()
		lista = list(positions[position].get_connections())

		positions[position].show_info()
		print("travel to where?")

		travel = input()

		if travel not in lista :
			print(travel + "not found")
			continue 

		partys[main_party].travel(positions[travel])

		print("--------------------")
		print("--------------------")





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
<<<<<<< Updated upstream:objetos.py
			party_dic[x[0]] = Party(x[0], x[1], int(x[2]) if int(x[2]) >= 1 else '1s', x[3])
=======
			#the strip is places in here to prevent save situation putting empty lines in the csv
			party_dic[x[0]] = Party(x[0], x[1], int(x[2]) if int(x[2]) >= 1 else '1s', x[3].strip())
>>>>>>> Stashed changes:Dungeon.py
			partys_names.append(x[0])


	enter_dungeon(position_dic, party_dic, partys_names)

main()