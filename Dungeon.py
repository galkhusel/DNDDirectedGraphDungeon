import random
import math
from Classes import Path, Room, Party, Adventurers
from ManageCSV import build_dungeon, save_situation
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

def main_party_encounters(encounter, partys, main_party):

	resolution = 1

	print(encounter)

	while resolution != "Finish":

		print("enter a resolution : Finish, kill, revive, change-sides, join_group, remove_group, logg, show")

		resolution = input()

		if resolution == "Finish":
			continue
		elif resolution == "show":
			for x in encounter:
				print(x)
				print(encounter[x].get_adventurers())
				continue

		print("enter position corresponding to party - ")
		print(encounter)
		party_input = input()

		if  party_input not in encounter:
			continue

		elif resolution == "join_group":
				new_party = partys.pop(party_input)
				main_party.add_party_group(new_party)
				continue

		elif resolution == "remove_group":
				print("enter party name to remove -")
				print(main_party.get_party_group())
				party_input = input()
				detached_party = main_party.remove_party_group(party_input)
				partys[detached_party.get_name()] = detached_party
				encounter[detached_party.get_name()] = detached_party
				continue

		elif resolution == "kill":
			encounter[party_input].set_alive(False)

		elif resolution == "revive":
			encounter[party_input].set_alive(True)

		elif resolution == "change-sides":
			value = input()
			if value != "True" or value != "False":
				encounter[party_input].set_side(ast.literal_eval(value))
			
			else:
				encounter[party_input].set_side("")
		elif resolution == "logg":
			print("logging")
			dungeon_logger.add_plain_text(input())


def confrontation(partys):
		
		"""if resolution == "add_adventurer":
			adventurers = party[party_input].get_adventurers()
			print(adventurers)
			party[party_input].get_adventurers(input())
			while select_adventurer != "Finish":
				
				party[main_party].add_adventurer(select_adventurer)
				adventurers = party[party_input].get_adventurers()
				print(adventurers)
				select_adventurer = input()
		"""
		
		"""
		elif resolution == "run":
			print(resolution)

		elif resolution == "enemies run":
			print(resolution)
		"""

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
		if len(encounters[x]) > 1 or main_party.get_name() in encounters[x]:
			deads = []
			if main_party.get_name() in encounters[x]:
				deads = main_party_encounters(encounters[x], partys, main_party)
				positions[x].add_deads(deads)
			else:
				deads = confrontation([partys[key] for key in encounters[x]])
				positions[x].add_deads(deads)

			dungeon_logger.add_encounter_history(x, encounters[x], deads)

def create_encounters_diccionary(main_party, partys):
	encounters = {}
	encounters[main_party.get_room().get_name()] = {main_party.get_name(): main_party}
	for x in partys:

		position = partys[x].get_room().get_name()

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
		actual_position = partys[p_name].get_room().get_name()
		print(actual_position)
		list_connections = make_connection_list(positions, actual_position)
		print(list_connections)
		partys[p_name].random_travel(positions)
		#adjusting power level of location
		actual_location = positions[partys[p_name].get_room().get_name()]

		dungeon_logger.add_travel_history(actual_location, p_name)
		print(partys[p_name].get_name())
		print(partys[p_name].get_room().get_name())
	return 1

# party tries to move to an adjacent place if it can move it adjust the power level of that place 
def main_party_travel(positions, main_party, travel):
	actual_position = main_party.get_room().get_name()
	list_ = list(positions[actual_position].get_connections())

	if travel in list_:
		#moving
		main_party.travel(positions[travel]) 	

		return True
	else:
		print(travel + "not found")
		return False

def enter_dungeon(positions, partys, main_party):
		
	travel = 1

	while travel != "Quit":

		positions[main_party.get_room().get_name()].show_info()
		print("travel to where?")
		print("enter a path or Quit")
		travel = input()



		if travel == "Quit":
			break

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

		#calculate_status(positions, main_party , partys)

		dungeon_logger

"""
====================================================================================================
====================================================================================================
								

											main

====================================================================================================					
====================================================================================================
"""

def main():

	dungeon_logger.add_plain_text("ONCE AGAIN WE ENTER THE DUNGEON")

	position_dic, party_dic, main_party = build_dungeon(
														"paths.csv", 
														"locations.csv", 
														"partys.csv", 
														"mainParty.csv", 
														"adventurers.csv",
														)

	enter_dungeon(
				position_dic, 
				party_dic, 
				main_party)

	print("saving progress")
	save_situation(
					position_dic, 
					party_dic, 
					main_party, 
					"paths.csv", 
					"locations.csv", 
					"partys.csv", 
					"mainParty.csv", 
					"adventurers.csv",
					)
	

if __name__ == '__main__':
	main()



