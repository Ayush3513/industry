"""Tests for the add_numbers module."""

import unittest
from test import add_numbers


class TestAddNumbers(unittest.TestCase):
    """Test cases for the add_numbers function."""

    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        self.assertEqual(add_numbers(1, 2), 3)

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        self.assertEqual(add_numbers(-1, -2), -3)

    def test_add_mixed_numbers(self):
        """Test adding a negative and a positive number."""
        self.assertEqual(add_numbers(-1, 2), 1)

    def test_add_zero(self):
        """Test adding zero to positive and zero values."""
        self.assertEqual(add_numbers(0, 5), 5)
        self.assertEqual(add_numbers(5, 0), 5)
        self.assertEqual(add_numbers(0, 0), 0)


if __name__ == "__main__":
    unittest.main()
