from unittest import TestCase

from pyplay.foo import concat_strings


class TestConcat(TestCase):
    def test_foo(self):
        result = concat_strings("Hello, ", "World!")
        self.assertEqual(result, "Hello, World!")
