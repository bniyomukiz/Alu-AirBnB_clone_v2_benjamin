#!/usr/bin/python3
""" Unit tests for BaseModel """
from models.base_model import BaseModel
import unittest
import datetime
import json
import os


class TestBaseModel(unittest.TestCase):
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        pass

    def tearDown(self):
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_default(self):
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            BaseModel(**copy)

    def test_save(self):
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        i = self.value()
        expected = '[{}] ({}) {}'.format(self.name, i.id, i.__dict__)
        self.assertEqual(str(i), expected)

    def test_todict(self):
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        n = {None: None}
        with self.assertRaises(TypeError):
            self.value(**n)

    def test_kwargs_one(self):
        n = {'Name': 'test'}
        with self.assertRaises(KeyError):
            self.value(**n)

    def test_id(self):
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)
