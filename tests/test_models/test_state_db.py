#!/usr/bin/python3
"""Unit test for State model using DB storage"""
import unittest
import os
import MySQLdb
from models import storage
from models.state import State


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "Only for DB storage")
class TestStateDB(unittest.TestCase):

    def setUp(self):
        """Set up MySQL connection before each test"""
        self.conn = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB'),
            port=3306
        )
        self.cursor = self.conn.cursor()

    def tearDown(self):
        """Tear down MySQL connection after each test"""
        self.cursor.close()
        self.conn.close()

    def test_insert_state(self):
        """Test if a new State is saved to the DB"""
        self.cursor.execute("SELECT COUNT(*) FROM states")
        count_before = self.cursor.fetchone()[0]

        new_state = State(name="California")
        new_state.save()

        self.cursor.execute("SELECT COUNT(*) FROM states")
        count_after = self.cursor.fetchone()[0]

        self.assertEqual(count_after, count_before + 1)
