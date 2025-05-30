
class BookManager:
    def __init__(self):
        self.books = {}
        self.next_id = 1

    def add_book(self, title, author, isbn, year=None):

        if not title or not isinstance(title, str):
            raise ValueError("Tytuł musi być niepustym ciągiem znaków")
        if not author or not isinstance(author, str):
            raise ValueError("Autor musi być niepustym ciągiem znaków")
        if not isbn or not isinstance(isbn, str):
            raise ValueError("ISBN musi być niepustym ciągiem znaków")
        if len(title) > 200:
            raise ValueError("Tytuł jest zbyt długi")

        book = {
            "title": title,
            "author": author,
            "isbn": isbn,
            "available": True
        }

        if year is not None:
            book["year"] = year


        book_id = self.next_id
        self.books[book_id] = book
        self.next_id += 1

        return book_id

    def remove_book(self, book_id):
        if book_id not in self.books:
            raise ValueError(f"Książka o ID {book_id} nie istnieje")
        del self.books[book_id]

    def get_book(self, book_id):
        if book_id not in self.books:
            raise ValueError(f"Książka o ID {book_id} nie istnieje")
        return self.books[book_id]

    def find_books_by_title(self, title):
        return [book for book_id, book in self.books.items()
                if title.lower() in book["title"].lower()]

    def find_books_by_author(self, author):
        return [book for book_id, book in self.books.items()
                if author.lower() in book["author"].lower()]

    def update_book(self, book_id, new_title=None, new_author=None, new_year=None):
        if book_id not in self.books:
            raise ValueError(f"Książka o ID {book_id} nie istnieje")

        book = self.books[book_id]

        if new_title:
            if not isinstance(new_title, str) or len(new_title) == 0:
                raise ValueError("Tytuł musi być niepustym ciągiem znaków")
            book["title"] = new_title

        if new_author:
            if not isinstance(new_author, str) or len(new_author) == 0:
                raise ValueError("Autor musi być niepustym ciągiem znaków")
            book["author"] = new_author

        if new_year is not None:
            book["year"] = new_year

        return True

    def list_books(self):
        return list(self.books.values())
