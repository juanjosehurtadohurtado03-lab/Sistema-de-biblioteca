import sqlite3

class Connection:
    def __init__(self, db_path: str = 'Library.db'):
        self.db_path = db_path
        self._get_table_books()
        self._get_table_authors()
        self._get_table_books_authors()
        self._get_table_lending()
        self._get_table_person()
        self._get_table_penalty()
    
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    
    def _get_table_books(self):
        with self._get_connection() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                copies INTEGER NOT NULL,
                status INTEGER DEFAULT 1
            )
            """)
    
    def _get_table_authors(self):
        with self._get_connection() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                status INTEGER DEFAULT 1
            )
            """)
    
    def _get_table_books_authors(self):
        with self._get_connection() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS book_author (
                book_id INTEGER NOT NULL,
                author_id INTEGER NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books(id) ON UPDATE CASCADE ON DELETE RESTRICT, 
                FOREIGN KEY (author_id) REFERENCES authors(id) ON UPDATE CASCADE ON DELETE RESTRICT,
                PRIMARY KEY (book_id, author_id)
            )
            """)
    
    def _get_table_lending(self):
        with self._get_connection() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS lendings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ci_person INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                init_lending TEXT NOT NULL,
                limit_lending TEXT NOT NULL,
                end_lending TEXT,
                status INTEGER DEFAULT 1,
                FOREIGN KEY (ci_person) REFERENCES persons(ci) ON UPDATE CASCADE ON DELETE RESTRICT,
                FOREIGN KEY (book_id) REFERENCES books(id) ON UPDATE CASCADE ON DELETE RESTRICT
            )
            """)
    
    def _get_table_person(self):
        with self._get_connection() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS persons (
                ci INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
            """)
    
    def _get_table_penalty(self):
        with self._get_connection() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS penalty (
                person_ci INTEGER PRIMARY KEY,
                amount REAL NOT NULL CHECK(amount > 0),
                status INTEGER DEFAULT 1,
                FOREIGN KEY (person_ci) REFERENCES persons(ci)
                    ON UPDATE CASCADE
                    ON DELETE RESTRICT
            )
            """)