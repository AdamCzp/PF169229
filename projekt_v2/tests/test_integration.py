import pytest
import os
import tempfile

from src.book_manager import BookManager
from src.category_manager import CategoryManager
from src.loan_manager import LoanManager
from src.reservation_manager import ReservationManager
from src.user_manager import UserManager
from src.utils import validate_email, validate_isbn, save_data, load_data


@pytest.fixture
def library_setup():
    book_manager = BookManager()
    user_manager = UserManager()
    category_manager = CategoryManager(book_manager)
    loan_manager = LoanManager(book_manager, user_manager)
    reservation_manager = ReservationManager(book_manager, user_manager)

    sample_user_id = user_manager.add_user("Jan Kowalski", "jan@example.com")
    sample_book_id = book_manager.add_book(
        "Władca Pierścieni", "J.R.R. Tolkien", "9788328705141", 1954
    )

    if "categories" not in book_manager.books[sample_book_id]:
        book_manager.books[sample_book_id]["categories"] = []

    if "Fantasy" not in category_manager.categories:
        category_manager.add_category("Fantasy")

    if "Science Fiction" not in category_manager.categories:
        category_manager.add_category("Science Fiction")

    return {
        "book_manager": book_manager,
        "user_manager": user_manager,
        "category_manager": category_manager,
        "loan_manager": loan_manager,
        "reservation_manager": reservation_manager,
        "sample_user_id": sample_user_id,
        "sample_book_id": sample_book_id,
    }


class TestLibrarySystemIntegration:
    def test_loan_book_integration(self, library_setup):
        lm = library_setup["loan_manager"]
        bm = library_setup["book_manager"]
        user_id = library_setup["sample_user_id"]
        book_id = library_setup["sample_book_id"]

        loan_id = lm.loan_book(user_id, book_id)
        book = bm.get_book(book_id)
        assert not book["available"]

        loan = lm.get_loan(loan_id)
        assert loan["user_id"] == user_id
        assert loan["book_id"] == book_id
        assert not loan["returned"]

    def test_return_book_integration(self, library_setup):
        lm = library_setup["loan_manager"]
        bm = library_setup["book_manager"]
        user_id = library_setup["sample_user_id"]
        book_id = library_setup["sample_book_id"]

        loan_id = lm.loan_book(user_id, book_id)
        lm.return_book(loan_id)

        book = bm.get_book(book_id)
        assert book["available"]

        loan = lm.get_loan(loan_id)
        assert loan["returned"]

    def test_assign_and_remove_category_integration(self, library_setup):
        cm = library_setup["category_manager"]
        bm = library_setup["book_manager"]
        book_id = library_setup["sample_book_id"]
        category_name = "Fantasy"

        cm.assign_category(book_id, category_name)
        book = bm.get_book(book_id)
        assert category_name in book["categories"]

        cm.remove_category_from_book(book_id, category_name)
        book = bm.get_book(book_id)
        assert category_name not in book["categories"]

    def test_remove_global_category_affecting_books(self, library_setup):
        cm = library_setup["category_manager"]
        bm = library_setup["book_manager"]
        book_id = library_setup["sample_book_id"]
        category_to_remove = "Science Fiction"

        cm.assign_category(book_id, category_to_remove)
        book = bm.get_book(book_id)
        assert category_to_remove in book["categories"]

        cm.remove_category(category_to_remove)

        book = bm.get_book(book_id)
        assert category_to_remove not in book["categories"]
        assert category_to_remove not in cm.categories

    def test_reserve_book_integration(self, library_setup):
        lm = library_setup["loan_manager"]
        rm = library_setup["reservation_manager"]
        um = library_setup["user_manager"]
        user1_id = library_setup["sample_user_id"]
        book_id = library_setup["sample_book_id"]

        lm.loan_book(user1_id, book_id)

        user2_id = um.add_user("Anna Nowak", "anna@example.com")
        reservation_id = rm.reserve_book(user2_id, book_id)
        reservation = rm.get_reservation(reservation_id)

        assert reservation["user_id"] == user2_id
        assert reservation["book_id"] == book_id
        assert reservation["status"] == "waiting"

    def test_book_returned_triggering_reservation(self, library_setup):
        lm = library_setup["loan_manager"]
        rm = library_setup["reservation_manager"]
        um = library_setup["user_manager"]
        user1_id = library_setup["sample_user_id"]
        book_id = library_setup["sample_book_id"]

        lm.loan_book(user1_id, book_id)
        user2_id = um.add_user("Anna Nowak", "anna@example.com")
        reservation_id = rm.reserve_book(user2_id, book_id)
        lm.return_book(lm.loans[next(iter(lm.loans))]["user_id"])

        triggered_reservation_id = rm.book_returned(book_id)
        assert triggered_reservation_id == reservation_id

        reservation = rm.get_reservation(reservation_id)
        assert reservation["status"] == "ready"
        assert reservation["notification_sent"]

    def test_complete_reservation_integration(self, library_setup):
        lm = library_setup["loan_manager"]
        rm = library_setup["reservation_manager"]
        um = library_setup["user_manager"]
        bm = library_setup["book_manager"]
        user1_id = library_setup["sample_user_id"]
        book_id = library_setup["sample_book_id"]

        loan_id_user1 = lm.loan_book(user1_id, book_id)
        user2_id = um.add_user("Anna Nowak", "anna@example.com")
        reservation_id_user2 = rm.reserve_book(user2_id, book_id)
        lm.return_book(loan_id_user1)
        rm.book_returned(book_id)

        book = bm.get_book(book_id)
        assert book["available"]
        rm.complete_reservation(reservation_id_user2)
        reservation = rm.get_reservation(reservation_id_user2)
        assert reservation["status"] == "completed"

    def test_utils_integration_with_user_manager(self, library_setup):
        um = library_setup["user_manager"]
        with pytest.raises(ValueError, match="Email musi być niepustym ciągiem znaków"):
            um.add_user("Test User Invalid", "")

        with pytest.raises(ValueError, match="Imię musi być niepustym ciągiem znaków"):
            um.add_user("", "test@example.com")

        user_id = um.add_user("Valid User", "prawidlowy@example.com")
        assert user_id is not None
        assert validate_email("prawidlowy@example.com")

    def test_utils_integration_with_book_manager(self, library_setup):
        bm = library_setup["book_manager"]
        with pytest.raises(ValueError, match="ISBN musi być niepustym ciągiem znaków"):
            bm.add_book("Test Book Invalid", "Test Author", "")

        book_id = bm.add_book("Valid Book", "Valid Author", "1234567890123")
        assert book_id is not None
        assert validate_isbn("1234567890123")

    def test_save_and_load_data_integration(self, library_setup):
        bm = library_setup["book_manager"]

        with tempfile.NamedTemporaryFile(
            delete=False, mode="w+", suffix=".json"
        ) as tmp_file:
            file_path = tmp_file.name

        try:
            test_data_simple = {"key": "value", "number": 123}
            save_data(test_data_simple, file_path)
            loaded_data = load_data(file_path)
            assert loaded_data == test_data_simple

            # Test with BookManager data
            book_id_A = bm.add_book("Book A for Save", "Author A", "111222333")
            book_id_B = bm.add_book("Book B for Save", "Author B", "444555666")

            books_to_save = {
                str(k): v for k, v in bm.books.items() if k in [book_id_A, book_id_B]
            }
            save_data(books_to_save, file_path)
            loaded_books = load_data(file_path)

            assert len(loaded_books) == 2
            assert loaded_books[str(book_id_A)]["title"] == "Book A for Save"
            assert loaded_books[str(book_id_B)]["author"] == "Author B"

        finally:
            if os.path.exists(file_path):
                os.unlink(file_path)

    def test_full_library_system_workflow(self, library_setup):
        um = library_setup["user_manager"]
        bm = library_setup["book_manager"]
        cm = library_setup["category_manager"]
        lm = library_setup["loan_manager"]
        rm = library_setup["reservation_manager"]

        user1_id = library_setup["sample_user_id"]
        user2_id = um.add_user("Anna Nowak Test Workflow", "anna.workflow@example.com")

        # 2. Add additional books
        book1_id = library_setup["sample_book_id"]
        book2_title = "Hobbit Edycja Testowa Workflow"
        book2_id = bm.add_book(book2_title, "J.R.R. Tolkien", "9780000000002", 1937)
        if "categories" not in bm.books[book2_id]:
            bm.books[book2_id]["categories"] = []
        fantasy_cat = "Fantasy"
        adventure_cat = "Przygodowa Test Workflow"
        if adventure_cat not in cm.categories:
            cm.add_category(adventure_cat)

        cm.assign_category(book1_id, fantasy_cat)
        cm.assign_category(book2_id, fantasy_cat)
        cm.assign_category(book2_id, adventure_cat)

        loan1_id = lm.loan_book(user1_id, book1_id)
        assert not bm.get_book(book1_id)["available"]

        reservation1_id = rm.reserve_book(user2_id, book1_id)
        assert rm.get_reservation(reservation1_id)["status"] == "waiting"
        assert rm.get_position_in_queue(reservation1_id) == 1

        lm.return_book(loan1_id)
        assert bm.get_book(book1_id)["available"]

        triggered_reservation_id = rm.book_returned(book1_id)
        assert triggered_reservation_id == reservation1_id
        reservation_details = rm.get_reservation(reservation1_id)
        assert reservation_details["status"] == "ready"
        assert reservation_details["notification_sent"]

        assert bm.get_book(book1_id)["available"]
        loan2_id = lm.loan_book(user2_id, book1_id)
        assert not bm.get_book(book1_id)["available"]

        rm.complete_reservation(reservation1_id)
        assert rm.get_reservation(reservation1_id)["status"] == "completed"

        lm.return_book(loan2_id)
        assert bm.get_book(book1_id)["available"]

        user2_reservations = rm.get_user_reservations(user2_id)
        active_reservations_for_book1_by_user2 = [
            res
            for res in user2_reservations
            if res["book_id"] == book1_id
            and res["status"] not in ["completed", "cancelled", "expired"]
        ]
        assert not active_reservations_for_book1_by_user2
