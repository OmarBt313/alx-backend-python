#!/usr/bin/env python3

import unittest
from utils import access_nested_map
"""Unit tests for the access_nested_map function."""

class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map."""

    def test_access_nested_map_valid_path(self):
        """Test access_nested_map with a valid path."""
        nested_map = {"a": {"b": {"c": 1}}}
        path = ["a", "b", "c"]
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, 1)

    def test_access_nested_map_valid_path_2(self):
        """Test access_nested_map with a different valid path."""
        nested_map = {"x": {"y": {"z": "hello"}}}
        path = ["x", "y", "z"]
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, "hello")

    def test_access_nested_map_invalid_key(self):
        """Test access_nested_map with an invalid key (should raise KeyError)."""
        nested_map = {"a": {"b": {"c": 1}}}
        path = ["a", "d"]  # "d" does not exist
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), "'d'")

    def test_access_nested_map_non_mapping(self):
        """Test access_nested_map when a path segment is not a Mapping."""
        nested_map = {"a": 1}  # "a" points to an integer, not a dict
        path = ["a", "b"]  # Can't access "b" from an integer
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), "'b'")

if __name__ == "__main__":
    unittest.main()


