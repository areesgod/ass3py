from src import *
import unittest 


class Testsimple(unittest.TestCase):
    def test_login(self):
        self.assertEqual(type(login(),function))


if __name__ == '__main__':
    unittest.main()

