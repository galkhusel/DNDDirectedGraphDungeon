import random

from Classes import Path, Location, Party, Adventurers
from ManageCSV import build_dungeon, save_situation

"""
====================================================================================================
====================================================================================================
								

								travelling in the dungeon functions

====================================================================================================					
====================================================================================================
"""

#adjust the power level by 1 depending if the party is allied or enemy , if neutral skips
def adjust_power_level(position, party):
	print("power_level")
	if party.get_adventurer != None:
		if party.get_adventurer() == True:
			position.set_power(True, 1)

		elif party.get_adventurer() == False:
			position.set_power(False, 1)


	return

# this function helps where where the parties can move
def make_connection_list(positions, actual_position):
	print("make_connection_list")
	list_aux = list(positions[actual_position].get_connections())
	list_connections = []
	for x in list_aux:
		list_connections.append(positions[x].get_names_powers())
	return list_connections

# all other parties tries to move to an adjacent place if they  can move it adjust the power level of that place accordingly
def other_party_movement(positions, partys):
	print("other_party_movement")

	for p_name in partys:
		if not partys[p_name].get_alive(): continue

		#moving
		actual_position = partys[p_name].get_location()
		list_connections = make_connection_list(positions, actual_position)
		partys[p_name].random_travel(list_connections)

		#adjusting power level of location
		actual_location = positions[partys[p_name].get_location()]
		adjust_power_level(actual_location, partys[p_name])

		print(partys[p_name].get_name() + partys[p_name].get_power() + " is in " + partys[p_name].get_location() + "its power is ")

	return 1

# party tries to move to an adjacent place if it can move it adjust the power level of that place 
def main_party_travel(positions, main_party, travel):
	print("main_party_travel")
	actual_position = main_party.get_location()
	list_ = list(positions[actual_position].get_connections())

	if travel in list_:
		#moving
		main_party.travel(positions[travel]) 
		
		#adjusting power level of location
		actual_location = positions[travel]
		adjust_power_level(actual_location, main_party)

	else:
		print(travel + "not found")

#refactor from here
def apply_damage(partys, damage):
	
	dead = []
	amount_partys = len(partys)
	counter_dead_partys = 0

	while damage > 0:

		party = random.choice(partys)

		if party.get_alive():
			actual_power = party.get_power() - damage
			deads = party.set_power(actual_power)
			for x in deads:
				dead.append(x)

		damage -= 1

	return dead

def calculate_outcome(partys, position_power):

	allies = 0
	allies_list = []

	enemies = 0
	enemies_list = []

	neutral = 0


	for x in partys:
		if x.get_side():
			allies += x.get_power()
			allies_list.append(x)

		elif not x.get_side():
			enemies += x.get_power()
			enemies_list.append(x)

		elif position.power > 0:
			neutral += x.get_power()


	return allies - enemies - position_power + neutral

def confrontation(partys, position_power):

	dead = []

	outcome = calculate_outcome(partys, position_power)

	damage = sqrt(outcome**2)

	if allies != 0 or enemies != 0:
		if outcome < 0:
			dead.append(apply_damage(allies_list, damage))

		if outcome > 0:
			dead.append(apply_damage(enemies_list, damage))

	return dead

def calculate_status(positions, partys):
	
	encounters = {}
	deads = []


	for x in partys:
		if partys[x].get_location() not in encounters:
			encounters[partys[x].get_location()] = [partys[x].get_name()]
		else:
			encounters[partys[x].get_location()].append(partys[x].get_name())

	for x in encounters:
		if len(encounters[x]) > 1:
			deads = confrontation([partys[key] for key in encounters[x] ] , position[x].get_power())
			positions[x].add_deads(deads)

#to here after making unit tests

def enter_dungeon(positions, partys, main_party):
		
	travel = 1

	while travel != "Quit":

		positions[main_party.get_location()].show_info()
		print("travel to where?")
		print("enter a path or Quit")
		travel = input()

		if travel == "Quit":
			break

		print("--------------------")
		print("--------------------")		
		print()
		print()
		print()
		print()
		other_party_movement(positions, partys)
		main_party_travel(positions, main_party, travel)
		calculate_status(partys, positions)

"""
====================================================================================================
====================================================================================================
								

											main

====================================================================================================					
====================================================================================================
"""

def main():

	position_dic, party_dic, main_party = build_dungeon("paths.csv", 
														"locations.csv", 
														"partys.csv", 
														"mainParty.csv", 
														"adventurers.csv")

	enter_dungeon(	position_dic, 
					party_dic, 
					main_party)

	print("saving progress")
	save_situation(	position_dic, 
					party_dic, main_party, 
					"paths.csv", 
					"locations.csv", 
					"partys.csv", 
					"mainParty.csv", 
					"adventurers.csv")

if __name__ == '__main__':
	main()