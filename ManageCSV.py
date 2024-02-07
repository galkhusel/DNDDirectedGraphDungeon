import csv
import datetime
import json

import ast

from Classes import Path, Location, Party, Adventurers


PATH_LOAD = "Dungeon\\"
PATH_SAVE = "Dungeon_Updated\\"

"""
====================================================================================================
====================================================================================================
								

								building dungeon functions


====================================================================================================					
====================================================================================================
"""
def build_location(pathscsv, locationscsv):

	position_dic = {}

	with open(PATH_LOAD + pathscsv) as path, open(PATH_LOAD + locationscsv) as location:

		paths = csv.reader(path)
		locations = csv.reader(location)


		for x in locations:
			if len(x) > 0 :
				position_dic[x[0]] = Location(
					name = x[0],
					data = x[1],
					)

		for x in paths:
			if len(x) > 0 :			
				p = Path(

					origin = x[0],
					destination = x[1],
					name = x[2],
					data = x[3],
					)

			position_dic[p.get_name()] = p
			position_dic[p.get_origin()].add_path(p)


	return position_dic

def build_partys(partyscsv, mainpcsv, adventurerscsv):

	main_party = None
	party_dic = {}

	with open(PATH_LOAD + partyscsv) as party, open(PATH_LOAD + mainpcsv) as mp, open(PATH_LOAD + adventurerscsv) as adven:

		partys = csv.reader(party)
		mparty = csv.reader(mp)
		adventurers = csv.reader(adven)		


		for x in partys:
			if len(x) > 0 :
				#the strip is places in here to prevent save situation putting empty lines in the csv
				party_dic[x[0]] = Party(
					name = x[0],
					description = x[1],
					location = x[4],
					side = ast.literal_eval(x[5]),
					alive = ast.literal_eval(x[6].strip()),
					)

		for x in adventurers:
			if len(x) > 0 :
				print(x[4])

				if x[4] in party_dic:
					adv = Adventurers(
						name = x[0], 
						health = x[1], 
						max_health = x[2],  
						alive = ast.literal_eval(x[3]),
						cr = ast.literal_eval(x[5])
						)
				
					party_dic[x[4]].add_adventurer(adv)

		main = next(mparty)

		main_party =  Party(
				name = main[0],
				description = main[1],
				location = main[2],
				side = ast.literal_eval(main[3].strip()),
				alive = True,
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


def save_situation_adventurers(party_dic, adventurerscsv, date):


	with open(PATH_SAVE + date+adventurerscsv, 'a', newline='') as party:

		writer = csv.writer(party)


		for x in party_dic:

			adventurers = party_dic[x].get_adventurers()
			for adventurer in adventurers:
			

				row = [	
					adventurers[adventurer].get_name(),
					adventurers[adventurer].get_health(),
					adventurers[adventurer].get_max_health(),
					adventurers[adventurer].get_cr(),
					adventurers[adventurer].get_alive(),
					x,
				]
				
				print(row)
				writer.writerow(row)

	return 1

def save_situation_main(main_party, maincsv, date):

	with open(PATH_SAVE + date+maincsv, 'a', newline='') as mainparty:

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

	with open(PATH_SAVE + date+partyscsv, 'a', newline='') as party:

		writer = csv.writer(party)
		#print(party_dic)
		for x in party_dic:
			
			row = [
				party_dic[x].get_name(),
				party_dic[x].get_description(),
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
		])

def writelocation(location_object , location):
	
	location.writerow([
		location_object.get_name(),
		location_object.get_data(),
		])

def save_situation_position(position_dic, pathcsv, locationcsv, date):

	with open(PATH_SAVE + date+pathcsv, 'a', newline='') as path, open(PATH_SAVE + date+locationcsv, 'w', newline='') as location :

		paths = csv.writer(path)
		locations = csv.writer(location)


		for x in position_dic:
			
			if x.isdigit():
				writelocation(position_dic[x], locations)

			else:
				writepath(position_dic[x], paths)

	return 1

def save_situation(position_dic, party_dic, main_party, pathcsv, locationcsv, partyscsv, maincsv, adventurerscsv):

	date = str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M'))
	save_situation_adventurers(party_dic, adventurerscsv, date)
	save_situation_main(main_party, maincsv, date)
	save_situation_party(party_dic, partyscsv, date)
	save_situation_position(position_dic, pathcsv, locationcsv, date)