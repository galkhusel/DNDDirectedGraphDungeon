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
		self.dic = {"room" : [Room, Room_csv, ['name', 'description', 'deads']],
			  		"path" : [Path, Path_csv, ['name', 'description', 'deads', 'origin', 'destination']],
					"party" : [Party, Party_csv, ['name', 'description', 'room', 'side', 'alive']],
					"adventurers" : [Adventurers, Adventurers_csv, ['name', 'health', 'max_health', 'cr', 'alive', 'heal_capacity']],
					"mainParty" : [Party, MainParty_csv, ['name', 'description', 'room', 'side', 'alive']]}
		self.dungeon = {}
		
	def add_path_to_rooms(self, class_dictionary):

		for path in class_dictionary["path"]:
			origin = class_dictionary["path"][path].get_origin()
			class_dictionary["room"][origin].add_path(class_dictionary["path"][path])
			

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
		self.dungeon = class_dictionary
		return self.dungeon
	
	def formar_diccionario(self, position_dic, party_dic, main_party):
		
		room_dic = {}
		path_dic = {}
		Adventurers_csv = {}

		for x in party_dic:
			Adventurers_csv[x] = party_dic[x]

		for x in position_dic:
			if x.isdigit():
				path_dic[x] = position_dic[x]
			else:
				room_dic[x] = position_dic[x]

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
					object = [self.dungeon[class_][entity].get(attribute) for attribute in self.dic[class_][3]]
					data[object[0]] = object[1:]
				json.dump(data, j)