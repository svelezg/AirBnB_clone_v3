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
from io import StringIO
import contextlib
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

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""


class TestDBStorage_NewMethods_v3(unittest.TestCase):
    """Tests for methods added in V3 db_storage"""

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "not testing db storage")
    def test_dbs_get(self):
        """Test for the method to retrieve one object"""
        new_state = State(name="California")
        models.storage.new(new_state)
        new_state.save()
        first_state_id = list(models.storage.all("State").values())[0].id
        self.assertEqual(models.storage.get(
            "State", first_state_id).__class__.__name__, 'State')
        temp_stdout1 = StringIO()
        with contextlib.redirect_stdout(temp_stdout1):
            print("First state: {}".format(models.storage.get("State",
                                                              first_state_id)))
        output = temp_stdout1.getvalue().strip()
        self.assertIn(first_state_id, output)
        new_state = State(name="Michigan")
        new_state.save()
        new_user = User(email="amanda@gmail.com", password="my_pass")
        new_user.save()
        self.assertIs(new_state, models.storage.get("State", new_state.id))
        self.assertIs(None, models.storage.get("State", "blabla"))
        self.assertIs(None, models.storage.get("dummy_object", "blabla"))
        self.assertIs(new_user, models.storage.get("User", new_user.id))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "not testing db storage")
    def test_dbs_count(self):
        """Test for the method to count the number of objects in storage"""
        self.assertIs(type(models.storage.count()), int)
        self.assertIs(type(models.storage.count("State")), int)
        temp_stdout1 = StringIO()
        with contextlib.redirect_stdout(temp_stdout1):
            print(models.storage.count())
        output1 = temp_stdout1.getvalue().strip()
        temp_stdout2 = StringIO()
        with contextlib.redirect_stdout(temp_stdout2):
            print(models.storage.count("State"))
        output2 = temp_stdout2.getvalue().strip()
        self.assertTrue(output1 >= output2)
        initial_count = models.storage.count()
        initial_state_count = models.storage.count('State')
        self.assertEqual(models.storage.count("dummy_object"), 0)
        new_state = State(name="Nebraska")
        new_state.save()
        new_user = User(email="luke@gmail.com", password="my_pass")
        new_user.save()
        self.assertEqual(models.storage.count("State"),
                         initial_state_count + 1)
        self.assertEqual(models.storage.count(), initial_count + 2)
