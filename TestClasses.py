import unittest
from datetime import datetime
from unittest.mock import patch
from io import StringIO

from Classes import Path, Location, Party, Adventurers

class TestLocation(unittest.TestCase):
    
    def setUp(self):
        self.location = Location('1', 'starting location', 10, 20, {10:"sarasa", 11:"sarasa111111"})
        
    def test_add_path(self):
        path = Path('start', 'end', 'path', 'path between start and end', 5, 15,  {10:"sarasa", 11:"sarasa111111"})
        self.location.add_path(path)
        self.assertIn('path', self.location.paths)
        
    def test_get_connections(self):
        path1 = Path('start', 'end1', 'path1', 'path between start and end1', 5, 15,  {10:"sarasa", 11:"sarasa111111"})
        path2 = Path('start', 'end2', 'path2', 'path between start and end2', 7, 18,  {10:"sarasa", 11:"sarasa111111"})
        self.location.add_path(path1)
        self.location.add_path(path2)
        self.assertCountEqual(['path1', 'path2'], self.location.get_connections())
        
    def test_show_info(self):
        expected_output = "currently in Location: 1\npaths[]\nstarting location\n"
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            self.location.show_info()
            self.assertEqual(fake_stdout.getvalue(), expected_output)
        
    def test_get_names_powers(self):
        self.assertCountEqual(['1', 10], self.location.get_names_powers())
        
    def test_get_name(self):
        self.assertEqual('1', self.location.get_name())
        
    def test_get_data(self):
        self.assertEqual('starting location', self.location.get_data())
        
    def test_get_power(self):
        self.assertEqual(10, self.location.get_power())
        
    def test_set_power(self):
        self.location.set_power(True, 1)
        self.assertEqual(9, self.location.get_power())
        self.location.set_power(False, 1)
        self.assertEqual(10, self.location.get_power())
        
    def test_get_max_power(self):
        self.assertEqual(20, self.location.get_max_power())

class TestPath(unittest.TestCase):
    
    def setUp(self):
        self.path = Path('start', 'end', 'path', 'path between start and end', 5, 15, {10:"sarasa", 11:"sarasa111111"})
        
    def test_get_connections(self):
        self.assertCountEqual(['start', 'end'], self.path.get_connections())
        
    def test_get_name(self):
        self.assertEqual('path', self.path.get_name())
        
    def test_show_info(self):
        expected_output = "currently in path: path\norigin : start - destination : end\npath between start and end\n"
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            self.path.show_info()
            self.assertEqual(fake_stdout.getvalue(), expected_output)
        
    def test_get_names_powers(self):
        self.assertCountEqual(['path', 5], self.path.get_names_powers())
        
    def test_get_origin(self):
        self.assertEqual('start', self.path.get_origin())
        
    def test_get_destination(self):
        self.assertEqual('end', self.path.get_destination())
        
    def test_get_data(self):
        self.assertEqual('path between start and end', self.path.get_data())
        
    def test_get_power(self):
        self.assertEqual(5, self.path.get_power())
        
    def test_set_power(self):
        self.path.set_power(True, 1)
        self.assertEqual(4, self.path.get_power())
        self.path.set_power(False, 1)
        self.assertEqual(5, self.path.get_power())
        
    def test_get_max_power(self):
        self.assertEqual(15, self.path.get_max_power())

class TestAdventurer(unittest.TestCase):

    def setUp(self):
        self.adventurer = Adventurers("tannae", 85, 999, {"gear" : ["magic", "items"], "consumables" : ["potions", "scrolls"], "common" : ["backpack"], "crafting" : {"herbs" : 4, "ore" : 5}} ,True)

    def test_calculate_damage(self):
        self.adventurer.calculate_damage(-85)
        self.assertEqual(self.adventurer.get_health(), 0)
        self.assertEqual(self.adventurer.get_alive(), False)

class TestParty(unittest.TestCase):

    def setUp(self):
        self.adventurer1 = Adventurers("tannae", 85, 999, {"gear" : ["magic", "items"], "consumables" : ["potions", "scrolls"], "common" : ["backpack"], "crafting" : {"herbs" : 4, "ore" : 5}} ,True)
        self.adventurer2 = Adventurers("tannae2", 85, 999, {"gear" : ["magic", "items"], "consumables" : ["potions", "scrolls"], "common" : ["backpack"], "crafting" : {"herbs" : 4, "ore" : 5}} ,True)
        self.location = Location('1', 'starting location', 5, 8, {10:"sarasa", 11:"sarasa111111"})
        self.adv = {self.adventurer1.get_name(): self.adventurer1, self.adventurer2.get_name() : self.adventurer2}
        self.party = Party("Party 1", "Some description", 5, 7, "1" , True, self.adv, True)

    def test_get_location(self):
        self.assertEqual(self.party.get_location(), "1")

    def test_get_name(self):
        self.assertEqual(self.party.get_name(), "Party 1")

    def test_get_power(self):
        self.assertEqual(self.party.get_power(), 5)

    def test_get_description(self):
        self.assertEqual(self.party.get_description(), "Some description")

    def test_get_side(self):
        self.assertEqual(self.party.get_side(), True)

    def test_travel(self):
        self.new_location = Location("2", "Some data", 6, 12, {10:"sarasa", 11:"sarasa111111"})
        self.party.travel(self.new_location)
        self.assertEqual(self.party.get_location(), "2")

    def test_random_travel_from_location(self):
        places = [("p2", 3), ("p3", 8)]
        self.party.random_travel(places)
        self.assertEqual(self.party.get_location(), "p2")
        self.assertEqual(self.party.get_power(), 4)

    def test_random_travel_with_insufficient_power_from_location(self):
        places = [("p2", 3), ("p3", 8)]
        self.party.set_power(2)
        self.party.set_location("1")
        self.party.random_travel(places)
        self.assertEqual(self.party.get_power(), 3)
        self.assertEqual(self.party.get_location(), "1")

    def test_random_travel_from_Path_going_ahead(self):
        places = [("1", 3), ("3", 5)]
        self.party.set_location("p2")
        self.party.set_power(5)
        self.party.random_travel(places)
        self.assertEqual(self.party.get_location(), "3")
        self.assertEqual(self.party.get_power(), 4)

    def test_random_travel_with_insufficient_power_from_Path(self):
        places = [("1", 3), ("3", 8)]
        self.party.set_location("p2")
        self.party.set_power(2)
        self.party.random_travel(places)
        self.assertEqual(self.party.get_power(), 3)
        self.assertEqual(self.party.get_location(), "p2")

    def test_random_travel_from_Path_going_backwards(self):
        places = [("1", 3), ("3", 8)]
        self.party.set_location("p2")
        self.party.set_power(7)
        self.party.random_travel(places)
        self.assertEqual(self.party.get_location(), "1")
        self.assertEqual(self.party.get_power(), 6)

    def test_set_power(self):
        self.party.set_power(10)
        self.assertEqual(self.party.get_power(), 10)

    def test_set_power_character_damage(self):
        self.party.set_power(-1)
        adv1 = self.party.get_adventurers()[self.adventurer1.get_name()]
        adv2 = self.party.get_adventurers()[self.adventurer2.get_name()]
        self.assertEqual(adv1.get_health() == 84 or adv2.get_health() == 84, True)

    def test_set_power_character_die(self):
        self.party.set_power(-85)
        adv1 = self.party.get_adventurers()[self.adventurer1.get_name()]
        adv2 = self.party.get_adventurers()[self.adventurer2.get_name()]
        self.assertEqual( not adv1.get_alive() or not adv2.get_alive(), True)

    def test_set_power_party_die(self):
        self.party.set_power(-85)
        self.party.set_power(-85)
        self.assertEqual(self.party.get_alive(), False)

class TestMain(unittest.TestCase):

    def setUp(self):
        self.location = Location("1", "Some data", 5, 8)
        self.party = Party("Party 1", "Some description", 5, 7, "1" , True, {"member1":  {"alive": True, "condition": "Normal"}, "member2": {"alive": False, "condition": "Dead"}})

if __name__ == '__main__':
    unittest.main()