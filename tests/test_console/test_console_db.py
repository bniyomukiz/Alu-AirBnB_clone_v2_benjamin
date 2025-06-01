#!/usr/bin/python3
"""Unittest for console create State in DBStorage"""

import unittest
import os
import MySQLdb
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "Only for DBStorage")
class TestConsoleDBState(unittest.TestCase):
    def setUp(self):
        """Connect to the test database"""
        self.db = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB'),
            charset="utf8"
        )
        self.cursor = self.db.cursor()

    def test_create_state_in_db(self):
        """Test that 'create State name="California"' adds a record"""
        self.cursor.execute("SELECT COUNT(*) FROM states;")
        before = self.cursor.fetchone()[0]

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="California"')

        self.cursor.execute("SELECT COUNT(*) FROM states;")
        after = self.cursor.fetchone()[0]

        self.assertEqual(after, before + 1)

    def tearDown(self):
        """Close the database connection"""
        self.db.close()
