from unittest import TestCase

from src.bdd.Module import Module
from src.parser.tools import calculate


class TestTools(TestCase):
    def test_calculate(self):
        module = Module(name="test_file.py", path="/home/pglandon/PycharmProjects/AutoComplete/tests/test_file.py")
        calculate(module)
        self.fail()
