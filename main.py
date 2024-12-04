import json
from typing import List, Dict, Union

DATA_FILE = "books.json"

def load_books() -> List[Dict[str, Union[int, str]]]:
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_books(books: List[Dict[str, Union[int, str]]]) -> None:
    with open(DATA_FILE, "w") as file:
        json.dump(books, file, indent=4)

def generate_id(books: List[Dict[str, Union[int, str]]]) -> int:
    return max([book["id"] for book in books], default=0) + 1

def add_book(title: str, author: str, year: str) -> None:
    books = load_books()
    new_book = {
        "id": generate_id(books),
        "title": title,
        "author": author,
        "year": year,
        "status": "в наличии"
    }
    books.append(new_book)
    save_books(books)
    print(f"Книга '{title}' добавлена успешно!")

def delete_book(book_id: int):
    books = load_books()
    books = [book for book in books if book["id"] != book_id]
    save_books(books)
    print(f"Книга с ID {book_id} удалена успешно!")

def search_books(query: str, field: str) -> List[Dict[str, Union[int, str]]]:
    books = load_books()
    return [book for book in books if query.lower() in book[field].lower()]

def list_books():
    books = load_books()
    if not books:
        print("Библиотека пуста.")
    else:
        for book in books:
            print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, "
                  f"Год: {book['year']}, Статус: {book['status']}")

def update_status(book_id: int, new_status: str):
    if new_status not in ["в наличии", "выдана"]:
        print("Ошибка: недопустимый статус.")
        return
    books = load_books()
    for book in books:
        if book["id"] == book_id:
            book["status"] = new_status
            save_books(books)
            print(f"Статус книги с ID {book_id} изменен на '{new_status}'.")
            return
    print(f"Ошибка: книга с ID {book_id} не найдена.")

def main():
    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания книги: ")
            add_book(title, author, year)
        elif choice == "2":
            book_id = int(input("Введите ID книги для удаления: "))
            delete_book(book_id)
        elif choice == "3":
            field = input("Введите поле для поиска (title, author, year): ")
            query = input("Введите строку для поиска: ")
            results = search_books(query, field)
            if results:
                for book in results:
                    print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, "
                          f"Год: {book['year']}, Статус: {book['status']}")
            else:
                print("Книги не найдены.")
        elif choice == "4":
            list_books()
        elif choice == "5":
            book_id = int(input("Введите ID книги для изменения статуса: "))
            new_status = input("Введите новый статус (в наличии, выдана): ")
            update_status(book_id, new_status)
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Ошибка: недопустимый выбор.")

if __name__ == "__main__":
    main()
