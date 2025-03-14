import unittest
from src.validate_email import validate_email

class TestValidateEmail(unittest.TestCase):
    def setUp(self):
        pass

    def test_email_positive(self):
        self.assertTrue(validate_email("info@wp.pl"))

    def test_email_negative(self):
        self.assertFalse(validate_email("info@"))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

