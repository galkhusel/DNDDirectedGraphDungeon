import unittest
from datetime import datetime
from unittest.mock import patch
from io import StringIO

from Classes import Path, Room, Party, Adventurers

class TestRoom(unittest.TestCase):
    
    def setUp(self):
        self.Room = Room('1', 'starting location')
        
    def test_add_path(self):
        path = Path('path','start', 'end',  'path between start and end')
        self.Room.add_path(path)
        self.assertIn('path', self.Room.get_connections())
        
    def test_get_connections(self):
        path1 = Path('path1', 'start', 'end1', 'path between start and end1')
        path2 = Path('path2', 'start', 'end2', 'path between start and end2')
        self.Room.add_path(path1)
        self.Room.add_path(path2)
        self.assertCountEqual(['path1', 'path2'], self.Room.get_connections())
        
    def test_show_info(self):
        expected_output = "currently in Room: 1\npaths[]\nstarting location\n[]\n"
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            self.Room.show_info()
            self.assertEqual(fake_stdout.getvalue(), expected_output)
        
        
    def test_get_name(self):
        self.assertEqual('1', self.Room.get_name())
        
    def test_get_data(self):
        self.assertEqual('starting location', self.Room.get_data())

class TestPath(unittest.TestCase):
    
    def setUp(self):
        self.path = Path('path','start', 'end', 'path between start and end')
        
    def test_get_connections(self):
        self.assertCountEqual(['start', 'end'], self.path.get_connections())
        
    def test_get_name(self):
        self.assertEqual('path', self.path.get_name())
        
    def test_show_info(self):
        expected_output = "currently in path: path\norigin : start - destination : end\npath between start and end\n[]\n"
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            self.path.show_info()
            self.assertEqual(fake_stdout.getvalue(), expected_output)
        

        
    def test_get_origin(self):
        self.assertEqual('start', self.path.get_origin())
        
    def test_get_destination(self):
        self.assertEqual('end', self.path.get_destination())
        
    def test_get_data(self):
        self.assertEqual('path between start and end', self.path.get_data())
        

class TestAdventurer(unittest.TestCase):

    def setUp(self):
        self.adventurer = Adventurers("tannae", 2, 5, 20, True, 2)

    def test_deal_damage(self):
        self.adventurer.deal_damage(1)
        self.assertEqual(self.adventurer.get_health(), 1)
        self.assertEqual(self.adventurer.get_alive(), True)
    
    def test_self_heal(self):

        current_health = 2

        while self.adventurer.get_health() < self.adventurer.get_max_health() and current_health <= self.adventurer.get_max_health() :
            print(self.adventurer.get_health())
            print(current_health)
            self.assertEqual(self.adventurer.get_health(), current_health)
            self.adventurer.self_heal()
            current_health += 2


        print(self.adventurer.get_health())
        print(current_health)
        self.adventurer.self_heal()
        self.assertEqual(self.adventurer.get_health(), 5)


    def test_death(self):
        self.adventurer.deal_damage(6)
        self.assertEqual(self.adventurer.get_health(), 0)
        self.assertEqual(self.adventurer.get_alive(), False)
    


class TestParty(unittest.TestCase):

    def setUp(self):
        self.adventurer1 = Adventurers("tannae", 100, 150, 20, True, 2)
        self.adventurer2 = Adventurers("errol", 40, 57 , 5 ,True, 10)
        self.Room = Room('1', 'starting location')
        self.party = Party("Party 1", "Some description","1" , True, True)
        self.party.add_adventurer(self.adventurer1)
        self.party.add_adventurer(self.adventurer2)


    def test_get_location(self):
        self.assertEqual(self.party.get_Room(), "1")

    def test_get_name(self):
        self.assertEqual(self.party.get_name(), "Party 1")

    def test_get_description(self):
        self.assertEqual(self.party.get_description(), "Some description")

    def test_get_side(self):
        self.assertEqual(self.party.get_side(), True)

    def test_travel(self):
        self.new_location = Room("2", "Some data")
        self.party.travel(self.new_location)
        self.assertEqual(self.party.get_Room(), "2")

class TestMain(unittest.TestCase):

    def setUp(self):
        self.Room = Location("1", "Some data", 5, 8)
        self.party = Party("Party 1", "Some description", 5, 7, "1" , True, {"member1":  {"alive": True, "condition": "Normal"}, "member2": {"alive": False, "condition": "Dead"}})

if __name__ == '__main__':
    unittest.main()