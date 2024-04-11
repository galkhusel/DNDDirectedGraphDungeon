import random
import math
from Classes import Path, Room, Party, Adventurers
from ManageCSV import File
from Lore import Logger
import os
import ast
"""
====================================================================================================
====================================================================================================
								
								travelling in the dungeon functions
====================================================================================================					
====================================================================================================
"""
"""esto hay que chequear todo."""
dungeon_logger = Logger()
# this function returns where the parties can move
def make_connection_list(positions, actual_position):
	list_aux = list(positions[actual_position].get_connections())
	list_connections = []
	for x in list_aux:
		list_connections.append(positions[x].get_name())
	return list_connections
def apply_damage(partys, damage):
	
	# add how much damage main party can do
	dead = []
	amount_partys = len(partys)
	counter_dead_partys = 0
	while damage > 0:
		party = random.choice(partys)
		if party.get_alive():
			damage -= 1
	return dead
def create_party_lists(partys):
	allies = 0
	allies_list = []
	enemies = 0
	enemies_list = []
	for x in partys:
		if x.get_side():
			allies += x.get_power()
			allies_list.append(x)
		elif not x.get_side():
			enemies += x.get_power()
			enemies_list.append(x)
	return {"allies" :  (allies_list, allies),
			"enemies":	(enemies_list, enemies),
	}
def calculate_outcome(partys):

	return partys["allies"][1] - partys["enemies"][1]

def main_party_encounters(party, room):

	resolution = 1

	while resolution != "Finish":

		print("enter a resolution : Finish, kill, revive, logg")

		resolution = input()

		if resolution == "Finish":
			continue

		print("enter key in the position of the corresponding to party - ")
		print(party)
		party_input = input()

		if resolution == "kill":
			print("entre kill")
			party[party_input].party_destroy(room)


		elif resolution == "revive":
			print("entre kill")
			party[party_input].set_alive(True)

		elif resolution == "logg":
			print("logging")
			dungeon_logger.add_plain_text(input())

def confrontation(partys):
	#divide in if has main party or not

	dead = []
	print(partys)
	outcome = calculate_outcome(partys)
	if outcome < 0:
		apply_damage(partys["allies"], outcome)
	elif outcome > 0:
		apply_damage(partys["enemies"], outcome)
	
	return dead
def confrontation_outcomes(encounters, main_party,  partys, positions):

	for x in encounters:
		print(encounters[x])
		if len(encounters[x]) > 1:
			deads = []

			if main_party.get_name() in encounters[x]:
				deads = main_party_encounters(encounters[x], x)

			else:
				deads = confrontation([partys[key] for key in encounters[x]])

			if deads:
				for dead in deads:
					positions[x].add_deads(dead)

			dungeon_logger.add_encounter_history(x, encounters[x], deads)

def create_encounters_diccionary(main_party, partys):
	encounters = {}
	encounters[main_party.get_room()] = {main_party.get_name(): main_party}
	for x in partys:
		position = partys[x].get_room()
		if position in encounters:

			encounters[position][partys[x].get_name()] = partys[x]
		else:
			encounters[position] = {partys[x].get_name() : partys[x]}
	return encounters

def calculate_status(positions, main_party, partys):
	
	encounters = create_encounters_diccionary(main_party, partys)
	confrontation_outcomes(encounters, main_party,  partys, positions)

def other_party_movement(positions, partys):
	
	for p_name in partys:
		if not partys[p_name].get_alive(): continue
		print("other party movement")
		#moving
		actual_position = partys[p_name].get_room()
		print(actual_position)
		list_connections = make_connection_list(positions, actual_position)

		partys[p_name].random_travel(list_connections)


		actual_location = positions[partys[p_name].get_room()]

		dungeon_logger.add_travel_history(actual_location, p_name)
		print(partys[p_name].get_name())
		print(partys[p_name].get_room())
	return 1

# party tries to move to an adjacent place if it can move it adjust the power level of that place 
def main_party_travel(positions, main_party, travel):

	actual_position = main_party.get_room()
	list_ = list(positions[actual_position].get_connections())

	if travel in list_:
		#moving
		
		main_party.travel(positions[travel].get_name()) 	
		return True
	else:
		print(travel + "not found")
		return False
def enter_dungeon(positions, partys, main_party):
		
	travel = 1

	while travel != "Quit":
		print(main_party.get_room())
		positions[main_party.get_room()].show_info()
		print("travel to where?")
		print("enter a path or Quit")
		travel = input()
		print()
		print()
		print()
		print()
		print("--------------------")
		print("--------------------")	
		if main_party_travel(positions, main_party, travel) != True:
			continue
		
		dungeon_logger.add_travel_history(travel, main_party.get_name())
		
		other_party_movement(positions, partys)
		calculate_status(positions, main_party , partys)
		#dungeon_logger.resolve_round()

"""
====================================================================================================
====================================================================================================
								
											main
====================================================================================================					
====================================================================================================
"""






def main():

	dungeon_logger.add_plain_text("ONCE AGAIN WE ENTER THE DUNGEON")

	file = File("room.json", 
				"paths.json", 
				"partys.json", 
				"adventurers.json",
				"mainParty.json", 
				)

	dic_ = file.build()

	position_dic = dic_["room"] | dic_["path"]
	party_dic = dic_["party"]

	main_party_name = list(dic_["mainParty"].keys())[0]
	main_party = dic_["mainParty"][main_party_name]



	enter_dungeon(
				position_dic, 
				party_dic, 
				main_party)

	print("saving progress")


	file.save(
					position_dic, 
					party_dic, 
					main_party, 
					)
	

if __name__ == '__main__':
	main()