import pytest
from datetime import datetime, timedelta
from src.reservation_manager import ReservationManager


class DummyBookManager:
    def __init__(self):
        self.books = {}

    def add_book(self, book_id, available=False):
        self.books[book_id] = {"id": book_id, "available": available}

    def get_book(self, book_id):
        if book_id not in self.books:
            raise ValueError("Book not found")
        return self.books[book_id]


class DummyUserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id):
        self.users[user_id] = {"id": user_id}

    def get_user(self, user_id):
        if user_id not in self.users:
            raise ValueError("User not found")
        return self.users[user_id]


@pytest.fixture
def reservation_manager_setup():
    book_manager = DummyBookManager()
    user_manager = DummyUserManager()
    rm = ReservationManager(book_manager, user_manager)

    user_manager.add_user(1)
    book_manager.add_book(101, available=False)
    return rm, book_manager, user_manager


class TestReservationManager:
    def test_successful_reservation(self, reservation_manager_setup):
        rm, _, _ = reservation_manager_setup
        reservation_id = rm.reserve_book(1, 101)
        reservation = rm.get_reservation(reservation_id)
        assert reservation["user_id"] == 1
        assert reservation["book_id"] == 101
        assert reservation["status"] == "waiting"

    def test_duplicate_reservation(self, reservation_manager_setup):
        rm, _, _ = reservation_manager_setup
        rm.reserve_book(1, 101)
        with pytest.raises(
            ValueError, match="Użytkownik o ID 1 już zarezerwował książkę o ID 101"
        ):
            rm.reserve_book(1, 101)

    def test_cancel_reservation(self, reservation_manager_setup):
        rm, _, _ = reservation_manager_setup
        reservation_id = rm.reserve_book(1, 101)
        result = rm.cancel_reservation(reservation_id)
        assert result is True
        reservation = rm.get_reservation(reservation_id)
        assert reservation["status"] == "cancelled"

    def test_complete_reservation(self, reservation_manager_setup):
        rm, _, _ = reservation_manager_setup
        reservation_id = rm.reserve_book(1, 101)
        rm.book_returned(101)
        ready_reservation = rm.get_reservation(reservation_id)
        assert ready_reservation["status"] == "ready"

        result = rm.complete_reservation(reservation_id)
        assert result is True
        completed_reservation = rm.get_reservation(reservation_id)
        assert completed_reservation["status"] == "completed"

    def test_expired_reservation(self, reservation_manager_setup):
        rm, _, _ = reservation_manager_setup
        reservation_id = rm.reserve_book(1, 101)
        rm.book_returned(101)
        assert "expiry_date" in rm.reservations[reservation_id]
        rm.reservations[reservation_id]["expiry_date"] = (
            datetime.now() - timedelta(days=rm.reservation_expiry_days + 1)
        ).isoformat()

        expired_ids = rm.check_expired_reservations()
        assert reservation_id in expired_ids
        assert rm.reservations[reservation_id]["status"] == "expired"

    def test_position_in_queue(self, reservation_manager_setup):
        rm, book_manager, user_manager = reservation_manager_setup
        user_manager.add_user(2)
        book_manager.add_book(102, available=False)

        res1_id = rm.reserve_book(1, 102)
        res2_id = rm.reserve_book(2, 102)

        assert rm.get_position_in_queue(res1_id) == 1
        assert rm.get_position_in_queue(res2_id) == 2

    def test_reserve_unavailable_book_actually_available(
        self, reservation_manager_setup
    ):
        rm, book_manager, _ = reservation_manager_setup
        book_manager.books[101]["available"] = True
        with pytest.raises(ValueError, match="Książka o ID 101 jest już dostępna"):
            rm.reserve_book(1, 101)

    def test_reserve_book_user_not_found(self, reservation_manager_setup):
        rm, _, _ = reservation_manager_setup
        with pytest.raises(ValueError, match="Użytkownik o ID 999 nie istnieje"):
            rm.reserve_book(999, 101)

    def test_reserve_book_book_not_found(self, reservation_manager_setup):
        rm, _, _ = reservation_manager_setup
        with pytest.raises(ValueError, match="Książka o ID 999 nie istnieje"):
            rm.reserve_book(1, 999)

    def test_cancel_nonexistent_reservation(self, reservation_manager_setup):
        rm, _, _ = reservation_manager_setup
        with pytest.raises(ValueError, match="Rezerwacja o ID 999 nie istnieje"):
            rm.cancel_reservation(999)

    def test_cancel_already_cancelled_reservation(self, reservation_manager_setup):
        rm, _, _ = reservation_manager_setup
        reservation_id = rm.reserve_book(1, 101)
        rm.cancel_reservation(reservation_id)
        with pytest.raises(
            ValueError, match="Nie można anulować rezerwacji o statusie cancelled"
        ):
            rm.cancel_reservation(reservation_id)

    def test_complete_reservation_not_ready(self, reservation_manager_setup):
        rm, _, _ = reservation_manager_setup
        reservation_id = rm.reserve_book(1, 101)  # Status 'waiting'
        with pytest.raises(
            ValueError,
            match="Tylko rezerwacje o statusie 'ready' mogą być zrealizowane",
        ):
            rm.complete_reservation(reservation_id)

    def test_book_returned_no_queue(self, reservation_manager_setup):
        rm, book_manager, _ = reservation_manager_setup
        book_manager.add_book(103, available=False)
        assert rm.book_returned(103) is False

    def test_check_expired_reservations_no_ready_reservations(
        self, reservation_manager_setup
    ):
        rm, _, _ = reservation_manager_setup
        rm.reserve_book(1, 101)
        assert rm.check_expired_reservations() == []
