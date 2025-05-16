import pytest
from src.category_manager import CategoryManager


class DummyBookManager:
    def __init__(self):
        self.books = {}

    def add_book(self, book_id):
        self.books[book_id] = {"id": book_id, "categories": []}

    def get_book(self, book_id):
        if book_id not in self.books:
            raise ValueError("Book not found")
        return self.books[book_id]


@pytest.fixture
def category_manager_setup():
    book_manager = DummyBookManager()
    category_manager = CategoryManager(book_manager)

    book_manager.add_book(1)
    book_manager.add_book(2)
    return category_manager, book_manager


class TestCategoryManager:
    def test_add_category(self, category_manager_setup):
        cm, _ = category_manager_setup
        cm.add_category("Fantasy")
        assert "Fantasy" in cm.get_all_categories()

    def test_add_existing_category(self, category_manager_setup):
        cm, _ = category_manager_setup
        cm.add_category("Fantasy")
        with pytest.raises(ValueError, match="Category already exists"):
            cm.add_category("Fantasy")

    def test_remove_category(self, category_manager_setup):
        cm, bm = category_manager_setup
        cm.add_category("Sci-Fi")
        bm.add_book(3)
        cm.assign_category(3, "Sci-Fi")
        assert "Sci-Fi" in bm.get_book(3)["categories"]

        cm.remove_category("Sci-Fi")
        assert "Sci-Fi" not in cm.get_all_categories()
        assert "Sci-Fi" not in bm.get_book(3)["categories"]

    def test_remove_nonexistent_category(self, category_manager_setup):
        cm, _ = category_manager_setup
        with pytest.raises(ValueError, match="Category does not exist"):
            cm.remove_category("Horror")

    def test_assign_category_to_book(self, category_manager_setup):
        cm, bm = category_manager_setup
        cm.add_category("History")
        cm.assign_category(1, "History")  # book 1 is from setup
        book = bm.get_book(1)
        assert "History" in book["categories"]

    def test_assign_nonexistent_category_to_book(self, category_manager_setup):
        cm, _ = category_manager_setup
        with pytest.raises(ValueError, match="Category does not exist"):
            cm.assign_category(1, "Unknown")

    def test_assign_category_to_nonexistent_book(self, category_manager_setup):
        cm, _ = category_manager_setup
        cm.add_category("Science")
        with pytest.raises(ValueError, match="Book not found"):
            cm.assign_category(999, "Science")

    def test_remove_category_from_book(self, category_manager_setup):
        cm, bm = category_manager_setup
        cm.add_category("Drama")
        cm.assign_category(1, "Drama")
        assert "Drama" in bm.get_book(1)["categories"]

        cm.remove_category_from_book(1, "Drama")
        assert "Drama" not in bm.get_book(1)["categories"]

    def test_get_books_by_category(self, category_manager_setup):
        cm, bm = category_manager_setup
        cm.add_category("Adventure")
        cm.assign_category(1, "Adventure")
        cm.assign_category(2, "Adventure")

        bm.add_book(3)
        cm.add_category("Thriller")
        cm.assign_category(3, "Thriller")

        result = cm.get_books_by_category("Adventure")
        assert sorted(result) == sorted([1, 2])

    def test_get_books_by_nonexistent_category(self, category_manager_setup):
        cm, _ = category_manager_setup
        with pytest.raises(ValueError, match="Category does not exist"):
            cm.get_books_by_category("Nonexistent Category")

    def test_remove_category_from_book_not_assigned(self, category_manager_setup):
        cm, bm = category_manager_setup
        cm.add_category("Poetry")

        bm.books[1]["categories"] = ["ExistingCategory"]

        cm.remove_category_from_book(1, "Poetry")
        assert "Poetry" not in bm.get_book(1)["categories"]
        assert bm.get_book(1)["categories"] == ["ExistingCategory"]

    def test_assign_category_already_assigned_to_book(self, category_manager_setup):
        cm, bm = category_manager_setup
        cm.add_category("Tech")
        cm.assign_category(1, "Tech")
        book_categories_before = list(bm.get_book(1)["categories"])

        cm.assign_category(1, "Tech")
        book_categories_after = bm.get_book(1)["categories"]

        assert "Tech" in book_categories_after
        assert book_categories_after.count("Tech") == 1
        assert sorted(book_categories_after) == sorted(book_categories_before)
