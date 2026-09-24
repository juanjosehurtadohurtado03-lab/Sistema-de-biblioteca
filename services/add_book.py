from database.repo import SQLite_methods
import sqlite3
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

class Add_Book:
    def __init__(self, repo: SQLite_methods):
        self.repo = repo
    
    def info_book(self):
        # BOOKS
        while True:
            title = input('Ingrese el titulo del libro: ').strip().capitalize()
            if title:
                break
            else:
                logging.error('Debe ingresar un titulo.')
                continue
        while True:
            try:
                copies = int(input('Ingrese el numero de copias que tiene de esta libro: '))
                if copies <= 0:
                    logging.error('El numero de copias no puede ser de 0.')
                    continue
                break
            except ValueError:
                logging.error('Dato invalido.')
                continue
        
        # AUTHORS
        authors = set()
        while True:
            author = input('Ingrese un autor (o presione Enter para terminar): ').strip().title()
            if not author:
                if authors:
                    break
                logging.warning('Debe colocar al menos un autor para terminar.')
                continue
            
            if not author.replace(' ', '').isalpha():
                logging.error('El autor solo puede contener letras.')
                continue
            
            if author in authors:
                logging.warning(f'El autor {author} ya esta registrado.')
                continue
            
            authors.add(author)
        return title, copies, authors
    
    def add_book(self, title: str, copies: int, authors: set):
        books_ids = self.repo.search_book_name(title)
        if books_ids:
            for book_id in books_ids:
                existing_authors_set = self.repo.check_authors_from_book(book_id)
                if authors == existing_authors_set:
                    logging.warning(f'El libro {title} con los autores {authors} ya esta registrado.')
                    return None
        with self.repo.connection._get_connection() as conn:
            try:
                cursor = conn.cursor()
                # Insercion de libro devolviendo su id unico.
                book_id = self.repo.insert_book(cursor, title, copies)
                for author in authors:
                    result = self.repo.search_author(cursor, author)
                    if result is None:
                        author_id = (self.repo.insert_authors(cursor, author))
                    else:
                        author_id = result[0]
                    self.repo.insert_books_authors_intermediate(cursor, book_id, author_id)
                print(f'\nEl libro {title} ha sido registrado con exito. Su codigo es {book_id}.')
                conn.commit()
            except sqlite3.Error as e:
                logging.critical(f'Error en base de datos: {e}')
                conn.rollback()
