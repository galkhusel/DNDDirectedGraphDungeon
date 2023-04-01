import csv
import datetime

from Classes import Path, Location, Party, Adventurers

"""
====================================================================================================
====================================================================================================
								

								building dungeon functions


====================================================================================================					
====================================================================================================
"""
def build_location(paths, locations):

	position_dic = {}

	with open(paths) as path, open(locations) as location:

		paths = csv.reader(path)
		locations = csv.reader(location)


		for x in locations:
			position_dic[x[0]] = Location(
				name = x[0],
				data = x[1],
				power = int(x[2]) if int(x[2]) >= 0 else 0, 
				max_power = int(x[3]) if int(x[3]) >= 0 else int(x[2]) if int(x[2]) >= 0 else 0,
				status = x[4].strip()
				)

		for x in paths:
			p = Path(

				origin = x[0],
				destination = x[1],
				name = x[2],
				data = x[3],
				power = int(x[4]) if int(x[4]) >= 0 else 0,
				max_power = int(x[5]) if int(x[5]) >= 0 else int(x[4]) if int(x[4]) >= 0 else 0,
				status = x[6].strip()
				)

			position_dic[p.name] = p
			position_dic[p.origin].add_path(p)

	return position_dic

def build_partys(partys, mainp, adventurers):

	main_party = None
	party_dic = {}

	with open(partys) as party, open(mainp) as mp, open(adventurers) as adven:

		partys = csv.reader(party)
		mparty = csv.reader(mp)
		adventurer = csv.reader(adven)		

		for x in partys:
			
			#the strip is places in here to prevent save situation putting empty lines in the csv
			party_dic[x[0]] = Party(
				name = x[0],
				description = x[1],
				power = int(x[2]) if int(x[2]) >= 1 else '1',
				max_power = int(x[3]) if int(x[3]) >= 0 else int(x[2]) if int(x[2]) >= 0 else 1,
				location = x[4],
				side = x[5],
				alive = x[6].strip(),
				)

		for x in adventurer:

			if x[5] in party_dic:
				
				adv = adventurer(
					name = x[0], 
					health = x[1], 
					max_health = x[2],  
					status = x[3], 
					alive = x[4].strip())
			
				party_dic[x[5]].add_adventurer(adv)

		main = next(mparty)

		main_party =  Party(
				name = main[0],
				description = main[1],
				power = 999,
				max_power = 999,
				location = main[2],
				side = main[3],
				alive = main[4].strip(),
				)
		
		print(main_party.get_location())

	return party_dic, main_party

def build_dungeon(paths, locations, partys, mainp, Adventurers):

	position_dic = build_location(paths, locations)

	party_dic, main_party = build_partys(partys, mainp, Adventurers)

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

	with open(date+pathcsv, 'a', newline='') as path, open(date+locationcsv, 'w', newline='') as location :

		paths = csv.writer(path)
		locations = csv.writer(location)


		for x in position_dic:
			
			if x.isdigit():
				writelocation(position_dic[x], locations)

			else:
				writepath(position_dic[x], paths)

	return 1

def save_situation_main(main_party, maincsv, date):

	with open(date+maincsv, 'a', newline='') as mainparty:

		writer = csv.writer(mainparty)
		print(main_party)
			
		row = [main_party.get_name(),
			main_party.get_description(),
			main_party.get_power(),
			main_party.get_location(),
			main_party.get_adventurer()
			]
		writer.writerow(row)

	return 1

def save_situation_party(party_dic, partyscsv, date):

	with open(date+partyscsv, 'a', newline='') as party:

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

def save_situation_adventurers(party_dic, partyscsv, date):

	with open(date+partyscsv, 'a', newline='') as party:

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

	date = str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M'))
	save_situation_adventurers(party_dic, adventurerscsv, date)
	save_situation_main(main_party, maincsv, date)
	save_situation_party(party_dic, partyscsv, date)
	save_situation_position(position_dic, pathcsv, locationcsv, date)