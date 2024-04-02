#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        new_state = State(name="California")
        storage.new(new_state)
        storage.save()
        all_objs = storage.all()
        self.assertIsInstance(all_objs, dict)
        self.assertIn(new_state, all_objs.values())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        new = State(name="California")
        storage.new(new)
        storage.save()
        self.assertIn(new, storage.all().values())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        new_state = State(name="California")
        storage.new(new_state)
        storage.save()
        storage.reload()
        self.assertIn(new_state, storage.all().values())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """ Test that get method retirieve needed obj """
        new_state = State(name="test", id="test")
        new_state.save()
        to_get = storage.get("State", "test")
        self.assertEqual(new_state.name, to_get.name)
        self.assertEqual(new_state.created_at.year, to_get.created_at.year)
        self.assertEqual(new_state.created_at.month, to_get.created_at.month)
        self.assertEqual(new_state.created_at.day, to_get.created_at.day)
        self.assertEqual(new_state.created_at.hour, to_get.created_at.hour)
        self.assertEqual(new_state.created_at.minute, to_get.created_at.minute)
        self.assertEqual(new_state.created_at.second, to_get.created_at.second)
        storage.delete(new_state)
        to_get = storage.get("State", "test")
        self.assetIsNone(to_get)
        to_get = storage.get("Dummy", "test")
        self.assetIsNone(to_get)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count():
        """ test count method for db_stoarge"""
        test_length = len(storage.all())
        new_state = State(name="test1")
        new_state.save()
        self.assertEqual(test_length + 1, storage.count())
        second_state = State(name="test2")
        second_state.save()
        self.assertEqual(test_length + 2, storage.count())
