import unittest
from datetime import datetime
from unittest.mock import patch
from io import StringIO

from Dungeon import Path, Location, arty

class TestLocation(unittest.TestCase):
    
    def setUp(self):
        self.location = Location('1', 'starting location', 10, 20)
        
    def test_add_path(self):
        path = Path('start', 'end', 'path', 'path between start and end', 5, 15)
        self.location.add_path(path)
        self.assertIn('path', self.location.paths)
        
    def test_get_connections(self):
        path1 = Path('start', 'end1', 'path1', 'path between start and end1', 5, 15)
        path2 = Path('start', 'end2', 'path2', 'path between start and end2', 7, 18)
        self.location.add_path(path1)
        self.location.add_path(path2)
        self.assertCountEqual(['end1', 'end2'], self.location.get_connections())
        
    def test_show_info(self):
        expected_output = "currently in Location: start\npaths['path']\nstarting location\n"
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            self.location.show_info()
            self.assertEqual(fake_stdout.getvalue(), expected_output)
        
    def test_get_names_powers(self):
        self.assertCountEqual(['start', 10], self.location.get_names_powers())
        
    def test_get_name(self):
        self.assertEqual('start', self.location.get_name())
        
    def test_get_data(self):
        self.assertEqual('starting location', self.location.get_data())
        
    def test_get_power(self):
        self.assertEqual(10, self.location.get_power())
        
    def test_set_power(self):
        self.location.set_power(12)
        self.assertEqual(12, self.location.get_power())
        
    def test_get_max_power(self):
        self.assertEqual(20, self.location.get_max_power())

class TestPath(unittest.TestCase):
    
    def setUp(self):
        self.path = Path('start', 'end', 'path', 'path between start and end', 5, 15)
        
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
        self.path.set_power(8)
        self.assertEqual(8, self.path.get_power())
        
    def test_get_max_power(self):
        self.assertEqual(15, self.path.get_max_power())

class TestParty(unittest.TestCase):
    
    def setUp(self):
        self.location = Location('start', 'starting location', 10, 20)
        self.party = Party('party', 'adventurer party', 8, 15)
