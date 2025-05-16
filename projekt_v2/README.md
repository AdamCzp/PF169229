# System Zarządzania Biblioteką
Prosta aplikacja konsolowa do zarzadzania zbiorami  bibliotecznymi, użytkownikami, wypożyczeniami oraz rezerwacjami książek. System zarzadzania Biblioteka napisany w Python, z zestawem testów jednostkowych i integracyjnych.
## Spis treści

- [Opis projektu](#opis-projektu)
- [Główne funkcjonalności](#główne-funkcjonalności)
- [Struktura projektu](#struktura-projektu)
- [Wymagania](#wymagania)
- [Instalacja](#instalacja)
- [Uruchamianie testów](#uruchamianie-testów)
- [Użycie](#użycie)
- [Autor](#autor)

## Opis projektu

Celem projektu jest stworzenie aplikacji w języku Python do symulacji podstawowych operacji w systemie bibliotecznym. Aplikacja pozwala na zarządzanie katalogiem książek, rejestrację użytkowników, obsługę wypożyczeń i zwrotów, a także system rezerwacji dla niedostępnych pozycji. Kluczowym elementem projektu jest również kompleksowy zestaw testów jednostkowych i integracyjnych zapewniający poprawność działania poszczególnych modułów oraz ich współpracy.

## Główne funkcjonalności

Aplikacja realizuje następujące funkcjonalności:

* **Zarządzanie książkami:**
    * Dodawanie nowych książek (tytuł, autor, ISBN, rok wydania).
    * Usuwanie książek z katalogu.
    * Wyszukiwanie książek (po tytule, autorze).
    * Przeglądanie listy wszystkich książek.
    * Aktualizacja danych o książkach.
* **Zarządzanie użytkownikami:**
    * Dodawanie nowych użytkowników (imię, email).
    * Usuwanie użytkowników.
    * Wyszukiwanie użytkowników.
    * Przeglądanie listy użytkowników.
    * Aktualizacja danych użytkowników.
* **Zarządzanie kategoriami:**
    * Dodawanie nowych kategorii.
    * Usuwanie kategorii.
    * Przypisywanie kategorii do książek.
    * Usuwanie kategorii z książek.
    * Wyszukiwanie książek po kategorii.
* **Obsługa wypożyczeń:**
    * Wypożyczanie książek przez zarejestrowanych użytkowników.
    * Obsługa zwrotów książek.
    * Przeglądanie historii wypożyczeń.
* **System rezerwacji:**
    * Rezerwowanie książek, które są aktualnie wypożyczone.
    * Anulowanie rezerwacji.
    * Powiadamianie o dostępności zarezerwowanej książki (symulowane).
    * Zarządzanie kolejką rezerwacji.
* **Walidacja danych:**
    * Sprawdzanie poprawności wprowadzanych danych (np. format email, ISBN).
* **Utrwalanie danych:**
    * Zapis i odczyt stanu aplikacji (książki, użytkownicy, wypożyczenia, rezerwacje) do/z plików JSON.

## Struktura projektu

```

.
├── src/                      \# Katalog z kodem źródłowym aplikacji
│   ├── **init**.py
│   ├── book\_manager.py       \# Moduł zarządzania książkami
│   ├── user\_manager.py       \# Moduł zarządzania użytkownikami
│   ├── loan\_manager.py       \# Moduł zarządzania wypożyczeniami
│   ├── category\_manager.py   \# Moduł zarządzania kategoriami
│   ├── reservation\_manager.py \# Moduł zarządzania rezerwacjami
│   └── utils.py              \# Funkcje pomocnicze (np. walidacja, zapis/odczyt danych)
├── tests/                    \# Katalog z testami
│   ├── **init**.py
│   ├── test\_book\_manager.py
│   ├── test\_user\_manager.py
│   ├── test\_loan\_manager.py
│   ├── test\_category\_manager.py
│   ├── test\_reservation\_manager.py
│   ├── test\_utils.py
│   └── test\_integration.py   \# Testy integracyjne
├── .gitignore                \# Plik określający ignorowane pliki przez Git
├── README.md                 \# Ten plik
└── requirements.txt          \# Lista zależności projektu

````

## Wymagania

* Python 3.8+
* Biblioteki wymienione w pliku `requirements.txt` (głównie `pytest` i `pytest-cov` dla dewelopera/testera).

## Instalacja

1.  Sklonuj repozytorium:
    ```bash
    git clone https://github.com/AdamCzp/PF169229/tree/main/projekt_v2
    cd projekt
    ```
2.  (Zalecane) Utwórz i aktywuj wirtualne środowisko:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```
3.  Zainstaluj zależności:
    ```bash
    pip install -r requirements.txt
    ```

## Uruchamianie testów

Aby uruchomić wszystkie testy jednostkowe i integracyjne, wykonaj polecenie w głównym katalogu projektu:
```bash
pytest
````

Aby uruchomić testy wraz z generowaniem raportu pokrycia kodu (wyniki w terminalu oraz w katalogu `htmlcov/`):

```bash
pytest --cov=src --cov-report=html
```

## Użycie

System biblioteczny składa się z kilku managerów, które pozwalają na interakcję z danymi. Poniżej znajdują się podstawowe przykłady ich użycia w skrypcie Python.

### Inicjalizacja Managerów

Na początku należy zaimportować i utworzyć instancje odpowiednich managerów:
# Inicjalizacja managerów
```python
from src.book_manager import BookManager
from src.user_manager import UserManager
from src.category_manager import CategoryManager
from src.loan_manager import LoanManager
from src.reservation_manager import ReservationManager

book_manager = BookManager()
user_manager = UserManager()
category_manager = CategoryManager(book_manager) 
loan_manager = LoanManager(book_manager, user_manager)
reservation_manager = ReservationManager(book_manager, user_manager)
```


# Dodawanie książek
```python
try:
    book1_id = book_manager.add_book("Hobbit", "J.R.R. Tolkien", "9788324402940", 1937)
    book2_id = book_manager.add_book("Władca Pierścieni", "J.R.R. Tolkien", "9788377582117", 1954)
    print(f"Dodano książkę ID {book1_id}: {book_manager.get_book(book1_id)['title']}")
    print(f"Dodano książkę ID {book2_id}: {book_manager.get_book(book2_id)['title']}")
except ValueError as e:
    print(f"Błąd przy dodawaniu książki: {e}")
```

# Dodawanie kategorii
```python
try:
    category_manager.add_category("Fantasy")
    print("\nDodano kategorię: Fantasy")
except ValueError as e:
    print(f"Błąd przy dodawaniu kategorii: {e}")

# Przypisywanie kategorii do książek
try:
    category_manager.assign_category(book1_id, "Fantasy")
    category_manager.assign_category(book2_id, "Fantasy")
    print(f"Książka '{book_manager.get_book(book1_id)['title']}' ma kategorie: {book_manager.get_book(book1_id)['categories']}")
except ValueError as e:
    print(f"Błąd przy przypisywaniu kategorii: {e}")
```

# Listowanie książek w kategorii
```python
print("\nKsiążki w kategorii 'Fantasy':")
try:
    for book_id in category_manager.get_books_by_category("Fantasy"):
        print(f"- {book_manager.get_book(book_id)['title']}")
except ValueError as e:
    print(f"Błąd przy listowaniu książek w kategorii: {e}")
```
# Dodawanie użytkowników
```python
try:
    user1_id = user_manager.add_user("Alicja C.", "alicja@example.com")
    user2_id = user_manager.add_user("Bob M.", "bob@example.com")
    print(f"\nDodano użytkownika ID {user1_id}: {user_manager.get_user(user1_id)['name']}")
    print(f"Dodano użytkownika ID {user2_id}: {user_manager.get_user(user2_id)['name']}")
except ValueError as e:
    print(f"Błąd przy dodawaniu użytkownika: {e}")
```

# Listowanie użytkowników
```python
print("\nZarejestrowani użytkownicy:")
for user in user_manager.list_users():
    print(f"- {user['name']} ({user['email']})")
```

# Użytkownik 1 wypożycza książkę 1
```python
try:
    loan1_id = loan_manager.loan_book(user1_id, book1_id)
    print(f"\nKsiążka ID {book1_id} wypożyczona przez użytkownika ID {user1_id}. Dostępna: {book_manager.get_book(book1_id)['available']}")
except ValueError as e:
    print(f"Błąd przy wypożyczeniu: {e}")
```

# Użytkownik 2 próbuje wypożyczyć zajętą książkę 1, a następnie ją rezerwuje
```python
try:
    # Ta operacja powinna zgłosić błąd, ponieważ książka jest wypożyczona
    loan_manager.loan_book(user2_id, book1_id) 
except ValueError as e:
    print(f"Próba wypożyczenia książki ID {book1_id} przez użytkownika ID {user2_id} nieudana: {e}")
    # Skoro książka jest niedostępna, użytkownik 2 ją rezerwuje
    try:
        reservation1_id = reservation_manager.reserve_book(user2_id, book1_id)
        print(f"Książka ID {book1_id} zarezerwowana przez użytkownika ID {user2_id}. Pozycja w kolejce: {reservation_manager.get_position_in_queue(reservation1_id)}")
    except ValueError as reservation_error:
        print(f"Błąd przy rezerwacji: {reservation_error}")
```
# Użytkownik 1 zwraca książkę 1
```python
try:
    if 'loan1_id' in locals(): # Upewniamy się, że wypożyczenie miało miejsce
        loan_manager.return_book(loan1_id)
        print(f"\nKsiążka ID {book1_id} zwrócona. Dostępna: {book_manager.get_book(book1_id)['available']}")

        # System obsługuje zwrot i powiadamia o gotowej rezerwacji (jeśli istnieje)
        ready_reservation_id = reservation_manager.book_returned(book1_id)
        if ready_reservation_id:
            reserved_by_user_id = reservation_manager.get_reservation(ready_reservation_id)['user_id']
            print(f"Rezerwacja ID {ready_reservation_id} dla użytkownika ID {reserved_by_user_id} jest gotowa.")
            
            # Użytkownik, który miał rezerwację (user2_id), wypożycza książkę
            reservation_manager.complete_reservation(ready_reservation_id) 
            loan_manager.loan_book(reserved_by_user_id, book1_id) 
            print(f"Książka ID {book1_id} wypożyczona przez użytkownika ID {reserved_by_user_id} po rezerwacji. Dostępna: {book_manager.get_book(book1_id)['available']}")
except ValueError as e:
    print(f"Błąd przy zwrocie lub obsłudze rezerwacji: {e}")

```


## Autor

[Adam Czaplicki]
```
