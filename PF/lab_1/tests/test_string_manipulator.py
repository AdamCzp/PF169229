import unittest
from src.string_manipulator import StringManipulator

class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass
    def test_reverse_True(self):
        string = 'adda'
        string_manipulator = StringManipulator()
        self.assertEqual(string == string_manipulator.reverse(string), True)
    def test_reverse_False(self):
        string = 'add'
        string_manipulator = StringManipulator()
        self.assertEqual(string == string_manipulator.reverse(string), False)
    def test_stringcapitalize(self):
        string_manipulator = StringManipulator()
        self.assertEqual(string_manipulator.capitalize("hello") == "Hello", True)
    def test_stringcapitalize(self):
        string_manipulator = StringManipulator()
        self.assertIsNot(string_manipulator.capitalize("hello") == "Hello", True)

    def tearDown(self):
        pass




if __name__ == '__main__':
    unittest.main()
