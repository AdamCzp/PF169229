import unittest
from src.trip import Trip


class TestTripInitialization(unittest.TestCase):
    def test_trip_creation(self):
        trip = Trip("Paris", 7)
        self.assertEqual(trip.destination, "Paris")
        self.assertEqual(trip.duration, 7)

    def test_calculate_cost(self):
        trip = Trip("Paris", 7)
        self.assertEqual(trip.calculate_cost(), 700)

        trip = Trip("Rome", 5)
        self.assertEqual(trip.calculate_cost(), 500)

    def test_add_participant(self):
        trip = Trip("Paris", 7)
        trip.add_participant("John")
        self.assertIn("John", trip.participants)

        trip.add_participant("Alice")
        trip.add_participant("Bob")
        self.assertListEqual(trip.participants, ["John", "Alice", "Bob"])

    def test_add_empty_participant(self):
        trip = Trip("Paris", 7)
        with self.assertRaises(ValueError):
            trip.add_participant("")


if __name__ == "__main__":
    unittest.main()
