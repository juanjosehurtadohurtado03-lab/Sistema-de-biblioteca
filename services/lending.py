from models.logistics import Time
from database.repo import SQLite_methods
import sqlite3
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

class Lendings:
    def __init__(self, repo: SQLite_methods):
        self.repo = repo
    
    def select_book(self):
        # importar tuplas de libros
        books_list = self.repo.search_book_all()
        if not books_list:
            logging.info('No hay libros disponibles en estos momentos.')
            return
        # imprimir libros
        for book in books_list:
            print(f'ID:{book[0]} - {book[1]} | Author: {book[2]}.')
        # proceso de seleccion de libro -> book
        with self.repo.connection._get_connection() as conn:
            cursor = conn.cursor()
            while True:
                try:
                    option_id = int(input('\nIngrese el ID del libro que desees: '))
                    book_lending = self.repo.search_book_id(cursor, option_id)
                    # book_lendng = [id, title, authors]
                    if book_lending is None:
                        logging.error(f'ID invalido. No se encontro ningun ID: {option_id}.')
                        continue
                    num_copies = self.repo.search_books_copies(cursor, book_lending[0])
                    # num_copies = (copies)
                    if num_copies[0] <= 0:
                        logging.info('Este libro se agoto.')
                        return
                    print(f'Desea reservar el libro: {book_lending[1]} | {book_lending[2]}.\n')
                    return book_lending
                except ValueError:
                    logging.error('Dato invalido.')
                    continue
            
    def transaction(self, book_lending):
            # registrar persona
            with self.repo.connection._get_connection() as conn:
                cursor = conn.cursor()
                while True:
                    try:
                        ci = int(input('Ingrese su CI: '))
                        if len(str(ci)) == 8:
                            name = input('Ingrese su nombre: ').strip().title()
                            if name.replace(' ','').isalpha():
                                amount_penalty = self.repo.search_penalty(cursor, ci)
                                if amount_penalty:
                                    logging.warning(f'\nUsted tiene una penalizacion pendiente de {amount_penalty[0]}. No se le permite recibir libros hasta que la penalizacion sea pagada.\n')
                                    return
                                break
                            else:
                                logging.error('Solo se permiten letras.')
                        else:
                            logging.error('Dato invalido.')
                    except ValueError:
                        logging.error('Dato invalido')
                        continue
                try:
                    # verificar si la CI existe en persons.
                    # si no existe, entra en el if y lo inserta, si existe, sigue hacia el UPDATE directamente.
                    if self.repo.search_person_ci(cursor, ci) is None:
                        self.repo.insert_person(cursor, ci, name)
                    # entregamos el libro (-1)
                    num_copies = self.repo.search_books_copies(cursor, book_lending[0])
                    if num_copies[0] <= 0:
                        logging.info('Este libro se agoto.\n')
                        return
                    self.repo.update_copies_book(cursor, book_lending)
                    # preparando los datos para insert en lendings
                    now, time_limit = Time.time_init_and_limit()
                    self.repo.insert_lending(cursor, ci, book_lending, now, time_limit)
                    print(f'\nEl libro {book_lending[0]}: {book_lending[1]} ha sido entregado a {name} - {ci}.\n')
                    conn.commit()
                except sqlite3.Error as e:
                    logging.critical(f'Error en base de datos: {e}')
                    conn.rollback()