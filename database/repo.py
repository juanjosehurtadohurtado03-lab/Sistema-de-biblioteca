from database.connect import Connection
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

class SQLite_methods:
    def __init__(self, connection: Connection):
        self.connection = connection
    
    #* SEARCH:
    def search_book_all(self):
        with self.connection._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT 
                            books.id,
                            books.title,
                            GROUP_CONCAT (authors.name, ',') AS authors
                        FROM books
                        LEFT JOIN book_author ON books.id = book_author.book_id
                        LEFT JOIN authors ON authors.id = book_author.author_id
                        WHERE books.status = 1
                        GROUP BY books.id
                        ORDER BY books.title ASC
            """)
            return cursor.fetchall()
    
    def search_book_name(self, title: str):
        with self.connection._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM books WHERE status = 1 AND title = ?", (title,))
            return {row[0] for row in cursor.fetchall()}
    
    def search_book_id(self, cursor: Connection, book_id: int):
        cursor.execute("""SELECT books.id, books.title, authors.name
        FROM books LEFT JOIN book_author ON books.id = book_author.book_id
        LEFT JOIN authors ON authors.id = book_author.author_id
        WHERE books.status = 1 AND books.id = ?
        ORDER BY books.title ASC""", (book_id,))
        return cursor.fetchone()
    
    #* CURSOR ARGUMENT
    
    def search_books_copies(self, cursor: Connection, book_id: int):
        cursor.execute("SELECT copies FROM books WHERE id = ?", (book_id,))
        return cursor.fetchone()
    
    def search_author(self, cursor: Connection, author: str):
        cursor.execute("SELECT id FROM authors WHERE status = 1 AND name = ?", (author,))
        return cursor.fetchone()
    
    def search_bookID_personCI(self, cursor: Connection, ci: int, book_id: int):
            cursor.execute("""SELECT lendings.id, lendings.book_id, books.title 
                        FROM books JOIN lendings ON books.id = lendings.book_id
                        WHERE lendings.status = 1 AND lendings.ci_person = ? AND lendings.book_id = ?""", (ci, book_id))
            return cursor.fetchone()
    
    def search_person_ci(self, cursor: Connection, ci: int):
        cursor.execute("SELECT name, ci FROM persons WHERE ci = ?", (ci,))
        return cursor.fetchone()
    
    def search_limit_lending_time(self, cursor: Connection, id_row: int):
        cursor.execute("SELECT limit_lending FROM lendings WHERE status = 1 AND id = ?", (id_row,))
        return cursor.fetchone()
    
    def search_lendings_defeated_with_ID(self, lending_id: int):
        with self.connection._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT persons.name, persons.ci, books.title
                        FROM persons JOIN lendings ON persons.ci = lendings.ci_person
                        JOIN books ON books.id = lendings.book_id
                        WHERE id = ?""", (lending_id,))
            return cursor.fetchone()
    
    def search_lendings_all(self):
        with self.connection._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, limit_lending FROM lendings WHERE status = 1 AND end_lending IS NULL")
            return [list(row) for row in cursor.fetchall()]
    
    def search_penalty(self, cursor, ci):
        cursor.execute("""SELECT penalty.amount 
                    FROM penalty JOIN persons ON penalty.person_ci = persons.ci
                    WHERE penalty.status = 1 AND persons.ci = ?""", (ci,))
        return cursor.fetchone()

    #TODO insert_book process
    def insert_book(self, cursor: Connection, title: str, copies: int):
        cursor.execute("INSERT INTO books (title, copies) VALUES (?, ?)", (title, copies))
        return cursor.lastrowid
    
    def insert_authors(self, cursor: Connection, author: str):
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (author,))
        return cursor.lastrowid
    
    def check_authors_from_book(self, book_id: int):
        with self.connection._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT authors.name 
                        FROM book_author JOIN authors
                        ON book_author.author_id = authors.id 
                        WHERE authors.status = 1 AND book_author.book_id = ?""", (book_id,))
            return {row[0] for row in cursor.fetchall()}
    
    def insert_books_authors_intermediate(self, cursor: Connection, book_id: int, author_id: int):
        cursor.execute("INSERT INTO book_author (book_id, author_id) VALUES (?, ?)", (book_id, author_id))
    
    #TODO return_book process
    def select_books_from_ci(self, cursor: Connection, ci: int):
        cursor.execute("""SELECT books.id, books.title
                    FROM books 
                    JOIN lendings ON books.id = lendings.book_id
                    JOIN persons ON persons.ci = lendings.ci_person
                    WHERE lendings.status = 1 AND persons.ci = ?""", (ci,))
        return cursor.fetchall()
        
    
    def update_lendings_return_time(self, cursor: Connection, end_lending: str, id_row: int):
        cursor.execute("""UPDATE lendings SET end_lending = ?
                    WHERE id = ?""", (end_lending, id_row))
    
    def update_books_sum(self, cursor: Connection, id_row: int):
        cursor.execute("UPDATE books SET copies = copies + 1 WHERE id = ?", (id_row,))
    
    def update_status(self, cursor: Connection, id_row: int):
        cursor.execute("UPDATE lendings SET status = 0 WHERE status = 1 AND id = ?", (id_row,))
    
    def insert_penalty(self, cursor: Connection, person_ci: int, amount: float):
        cursor.execute("INSERT INTO penalty (person_ci, amount) VALUES (?, ?)", (person_ci, amount))
    
    #TODO lending process
    def insert_person(self, cursor: Connection, ci: int, name: str):
        cursor.execute("INSERT INTO persons (ci, name) VALUES (?, ?)", (ci, name))

    def update_copies_book(self, cursor: Connection, book_lending):
        cursor.execute("UPDATE books SET copies = copies - 1 WHERE id = ?", (book_lending[0],))

    def insert_lending(self, cursor: Connection, ci: int, book_lending, now: str, time_limit: str):
        cursor.execute("""INSERT INTO lendings (ci_person, book_id, init_lending, limit_lending)
        VALUES (?, ?, ?, ?)""", (ci, book_lending[0], now, time_limit))