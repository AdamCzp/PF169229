import unittest
from src.calculator import Calculator


class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass
    def test_calculator_add(self):
        calculator = Calculator()
        calculator.add(1, 2)
    def test_calculator_multiply(self):
        calculator = Calculator()
        calculator.mul(2, 3)
    def test_calculator_subtract(self):
        calculator = Calculator()
        calculator.sub(4,5)
    def test_calculator_divide(self):
        calculator = Calculator()
        calculator.div(2,0)
    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
