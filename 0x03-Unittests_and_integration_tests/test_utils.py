#!/usr/bin/env python3

import unittest
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    def test_access_nested_map(self):
        nested_map = {"a": {"b": {"c": 1}}}
        result = access_nested_map(nested_map, ["a", "b", "c"])
        self.assertEqual(result, 1)
    
