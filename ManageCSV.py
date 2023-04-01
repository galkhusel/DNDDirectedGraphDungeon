import csv
import datetime
import json

from Classes import Path, Location, Party, Adventurers

"""
====================================================================================================
====================================================================================================
								

								building dungeon functions


====================================================================================================					
====================================================================================================
"""
def build_location(pathscsv, locationscsv):

	position_dic = {}

	with open(pathscsv) as path, open(locationscsv) as location:

		paths = csv.reader(path)
		locations = csv.reader(location)


		for x in locations:
			if len(x) > 0 :
				position_dic[x[0]] = Location(
					name = x[0],
					data = x[1],
					power = int(x[2]) if int(x[2]) >= 0 else 0, 
					max_power = int(x[3]) if int(x[3]) >= 0 else int(x[2]) if int(x[2]) >= 0 else 0,
					status = x[4].strip()
					)

		for x in paths:
			if len(x) > 0 :			
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

def build_partys(partyscsv, mainpcsv, adventurerscsv, itemsjson):

	main_party = None
	party_dic = {}

	with open(partyscsv) as party, open(mainpcsv) as mp, open(adventurerscsv) as adven, open(itemsjson) as i:

		partys = csv.reader(party)
		mparty = csv.reader(mp)
		adventurers = csv.reader(adven)		
		items = json.load(i)


		for x in partys:
			if len(x) > 0 :
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

		for x in adventurers:
			if len(x) > 0 :
				print(x[4])

				if x[4] in party_dic:
					adv = Adventurers(
						name = x[0], 
						health = x[1], 
						max_health = x[2],  
						alive = x[3],
						status = items[x[0]] 
						)
				
					party_dic[x[4]].add_adventurer(adv)

		main = next(mparty)

		main_party =  Party(
				name = main[0],
				description = main[1],
				power = 999,
				max_power = 999,
				location = main[2],
				side = main[3].strip(),
				alive = True,
				)
		
		print(main_party.get_location())

	return party_dic, main_party

def build_dungeon(paths, locations, partys, mainp, Adventurers, items):

	position_dic = build_location(paths, locations)

	party_dic, main_party = build_partys(partys, mainp, Adventurers, items)

	return position_dic, party_dic, main_party

"""
====================================================================================================
====================================================================================================
								

								save instance functions

====================================================================================================					
====================================================================================================
"""

def save_situation_adventurers(party_dic, adventurerscsv, itemsjson, date):

	with open(date+adventurerscsv, 'a', newline='') as party,  open(date+itemsjson, 'a', newline='') as items:

		writer = csv.writer(party)

		dic_items = {}

		for x in party_dic:

			adventurers = party_dic[x].get_adventurers()
			for adventurer in adventurers:
				
				dic_items[adventurers[adventurer].get_name()] = adventurers[adventurer].get_status()

				row = [	
					adventurers[adventurer].get_name(),
					adventurers[adventurer].get_health(),
					adventurers[adventurer].get_max_health(),
					adventurers[adventurer].get_status(),
					adventurers[adventurer].get_alive(),
					x,
				]
				
				print(row)
				writer.writerow(row)

		json.dump(dic_items, items)

	return 1

def save_situation_main(main_party, maincsv, date):

	with open(date+maincsv, 'a', newline='') as mainparty:

		writer = csv.writer(mainparty)
		print(main_party)
			
		row = [
			main_party.get_name(),
			main_party.get_description(),
			main_party.get_location(),
			main_party.get_side(),
			]

		writer.writerow(row)

	return 1

def save_situation_party(party_dic, partyscsv, date):

	with open(date+partyscsv, 'a', newline='') as party:

		writer = csv.writer(party)
		#print(party_dic)
		for x in party_dic:
			
			row = [
				party_dic[x].get_name(),
				party_dic[x].get_description(),
				party_dic[x].get_power(),
				party_dic[x].get_max_power(),
				party_dic[x].get_location(),
				party_dic[x].get_side(),
				party_dic[x].get_alive(),
				]

			writer.writerow(row)

	return 1

def writepath(path_object , path):

	path.writerow([
		path_object.get_name(),
		path_object.get_origin(),
		path_object.get_destination(),
		path_object.get_data(),
		path_object.get_power(),
		path_object.get_max_power(),
		path_object.get_status(),
		])

def writelocation(location_object , location):
	
	location.writerow([
		location_object.get_name(),
		location_object.get_data(),
		location_object.get_power(),
		location_object.get_max_power(),
		location_object.get_status(),
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

def save_situation(position_dic, party_dic, main_party, pathcsv, locationcsv, partyscsv, maincsv, adventurerscsv, itemsjson):

	date = str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M'))
	save_situation_adventurers(party_dic, adventurerscsv, itemsjson, date)
	save_situation_main(main_party, maincsv, date)
	save_situation_party(party_dic, partyscsv, date)
	save_situation_position(position_dic, pathcsv, locationcsv, date)