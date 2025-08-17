from unittest import TestCase
from src.common.enums import NamingMode

class TestNamingMode(TestCase):
    def test_naming_mode(self):
        self.assertEqual(NamingMode.COPY, NamingMode("copy"))
        self.assertEqual(NamingMode.REPLACE, NamingMode("replace"))

    def test_naming_mode_values(self):
        self.assertIn("copy", NamingMode.choices())
        self.assertIn("replace", NamingMode.choices())

    def test_naming_mode_str(self):
        self.assertEqual(str(NamingMode.COPY), "copy")
        self.assertEqual(str(NamingMode.REPLACE), "replace")
