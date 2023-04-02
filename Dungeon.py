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

def apply_damage(partys, damage):
	
	# add how much damage main party can do

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

def create_party_lists(partys):

	allies = 0
	allies_list = []

	enemies = 0
	enemies_list = []

	neutral_list = []
	neutral = 0


	for x in partys:
		if x.get_side():
			allies += x.get_power()
			allies_list.append(x)

		elif not x.get_side():
			enemies += x.get_power()
			enemies_list.append(x)

		elif position.power > 0:
			neutral_list.append(x)
			neutral += x.get_power()

	return {"allies" :  (allies_list, allies),
			"enemies":	(enemies_list, enemies),
			"neutral":	(neutral_list, neutral),
	}

def calculate_outcome(partys, position_power):

	return partys[allies][1] - partys[enemies][1] - position_power + partys[neutral][1]

def confrontation(partys, position_power):


	#divide in if has main party or not

	dead = []

	partys_by_relationships = create_party_lists(partys)

	outcome = calculate_outcome(partys_by_relationships, position_power)

	damage = sqrt(outcome**2)

	if allies != 0 or enemies != 0:
		if outcome < 0:
			dead.append(apply_damage(partys_by_relationships["allies"][0], damage))

		if outcome > 0:
			dead.append(apply_damage(partys_by_relationships["enemies"][0], damage))

	return dead


def main_party_encounters(party):


	resolution = 1

	while resolution != "Finish":



		positions[main_party.get_location()].show_info()
		print("travel to where?")
		print("enter a path or Quit")
		travel = input()

		if resolution == "kill":

			party[input()].set_alive(False)

		if resolution == "restore":

			party[input()].set_alive(True)

		if resolution == "run"

			#chase?

		if resolution == "enemies run"

			#enemies move
		
		if resolution == "change sides"

			value = input()

			if value != "True" or value != "False"

				party[input()].set_side(ast.literal_eval(value))
			else:
				party[input()].set_side("")
		
		if resolution == "logg"

			#logg input




def calculate_status(positions, main_party, partys):
	
	encounters = {}
	deads = []


	# add main party to confrontations

	encounters[main_party.get_location()] = [main_party.get_name()]

	for x in partys:
		if partys[x].get_location() not in encounters:
			encounters[partys[x].get_location()] = partys[x]
		else:
			encounters[partys[x].get_location()].append(partys[x])



	for x in encounters:
		if len(encounters[x]) > 1:
			if main_party.get_name() not in encounters[x]:
				deads = confrontation([partys[key] for key in encounters[x]] , position[x].get_power())
				positions[x].add_deads(deads)

			else:
				deads = main_party_confrontation(party)



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
		calculate_status(partys, main_party , positions)

"""
====================================================================================================
====================================================================================================
								

											main

====================================================================================================					
====================================================================================================
"""

def main():

	position_dic, party_dic, main_party = build_dungeon(
														"paths.csv", 
														"locations.csv", 
														"partys.csv", 
														"mainParty.csv", 
														"adventurers.csv",
														"items.json")

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
					"items.json")

if __name__ == '__main__':
	main()