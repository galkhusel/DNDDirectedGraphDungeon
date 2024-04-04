import csv
import datetime
import json

import ast

from Classes import Path, Room, Party, Adventurers


PATH_LOAD = "Dungeon\\"
PATH_SAVE = "Dungeon_Updated\\"

"""
====================================================================================================
====================================================================================================
								

								building dungeon functions


====================================================================================================					
====================================================================================================
"""


class File:
	def __init__(self, Room_csv, Path_csv, Party_csv, Adventurers_csv, MainParty_csv):
		self.dic = {"room" : [Room, Room_csv, ["get_name", "get_data", "get_deads"]],
			  		"path" : [Path, Path_csv, ["get_name", "get_data", "get_deads", "get_origin", "get_destination"]],
					"party" : [Party, Party_csv, ["get_name", "get_description", "get_room", "get_side", "get_alive"]],
					"adventurers" : [Adventurers, Adventurers_csv, ["get_name", "get_health", "get_max_health", "get_cr", "get_alive", "get_heal_capacity"]],
					"mainParty" : [Party, MainParty_csv, ["get_name", "get_description", "get_room", "get_side", "get_alive"]]}
		self.dungeon = {}
		
	def add_path_to_rooms(self, class_dictionary):

		for path in class_dictionary["path"]:
			origin = class_dictionary["path"][path].get_origin()
			class_dictionary["room"][origin].add_path(class_dictionary["path"][path])
			
	def add_adventurers_to_party(self, dict):
		for x in dict["adventurers"]:
			dict["adventurers"][x]


	def build(self):
		
		class_dictionary = {}

		for class_ in self.dic:
			aux_dictionary = {}

			class_file_path = self.dic[class_][1]
			class_creator = self.dic[class_][0]

			with open(PATH_LOAD + class_file_path) as j:
				json_ = json.load(j)
				for key in json_:
					entity = json_[key]
					object_ = class_creator(key, *entity.values())
					aux_dictionary[object_.get_name()] = object_

			class_dictionary[class_] = aux_dictionary
		self.add_path_to_rooms(class_dictionary)
		self.add_adventurers_to_party(class_dictionary)
		self.dungeon = class_dictionary
		print(self.dungeon)
		return self.dungeon
	
	def formar_diccionario(self, position_dic, party_dic, main_party):
		
		room_dic = {}
		path_dic = {}
		Adventurers_csv = {}

		print(party_dic)
		for x in party_dic:
			print(x)
			print(party_dic[x].get_adventurers())
			for adventurer in party_dic[x].get_adventurers():
				print("entre")
				
				Adventurers_csv[adventurer] = party_dic[x].get_adventurers()[adventurer]
		print(Adventurers_csv)

		for x in position_dic:
			if x.isdigit():
				room_dic[x] = position_dic[x]
			else:
				path_dic[x] = position_dic[x]

		self.dungeon = {"path" : path_dic, 
						"room" : room_dic,
						"party" : party_dic,
						"adventurers" : Adventurers_csv,
						"mainParty" : main_party
						}

	def save(self, position_dic, party_dic,	main_party):
		
		self.formar_diccionario(position_dic , party_dic,	main_party)
		date = str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M'))
		
		for class_ in self.dic:
			class_file_path = self.dic[class_][1]
			with open(PATH_SAVE + date + class_file_path + ".json", "w") as j:
				data = {}
				for entity in self.dungeon[class_]:
					# la siguiente linea rompe.z
					object = [getattr(self.dungeon[class_][entity], method)() for method in self.dic[class_][2]]
					#esto flashea el formato
					data[object[0]] = object[1:]
				json.dump(data, j)