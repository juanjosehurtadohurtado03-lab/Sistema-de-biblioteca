from database.repo import SQLite_methods
from models.logistics import Time
import sqlite3
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

class Return:
    def __init__(self, repo: SQLite_methods):
        self.repo = repo
    
    def return_book(self):
        with self.repo.connection._get_connection() as conn:
            cursor = conn.cursor()
            while True:
                try:
                    ci = int(input('\nIngrese su CI: '))
                    person = self.repo.search_person_ci(cursor, ci)
                    # person = [name, ci]
                    if person is None:
                        logging.info('Esta CI no esta registrada.')
                        return
                    print(f'Persona: {person[0]} - {person[1]}.')
                    break
                except ValueError:
                    logging.error('Dato invalido.')
                    continue
            while True:
                try:
                    books_list = self.repo.select_books_from_ci(cursor, ci)
                    if not books_list:
                        logging.info('No tiene libros a su disposicion.')
                        return
                    for book in books_list:
                        print(f'ID: {book[0]} - {book[1]}.')
                    book_id = int(input('\nIngrese el ID del libro: '))
                    break
                except ValueError:
                    logging.error('Dato invalido.')
                    continue
        with self.repo.connection._get_connection() as conn:
            try:
                cursor = conn.cursor()
                amount_penalty = 0
                book = self.repo.search_bookID_personCI(cursor, ci, book_id)
                # book = [id, book_id, title]
                if book is None:
                    logging.info('No hay registro de prestamo de este libro a su nombre.')
                    return
                # person = [0: name, 1: ci]: book = [0: id, 1: title].
                print(f'\n{person[0]} - {person[1]}: ({book[1]}: {book[2]})\n')
                end_lending_time = Time.time_now()
                limit_lending_time = self.repo.search_limit_lending_time(cursor, book[0])
                amount_penalty_time = Time.time_diference(end_lending_time, limit_lending_time[0])
                if amount_penalty_time:
                    amount_penalty = Time.penalty(amount_penalty_time)
                self.repo.update_lendings_return_time(cursor, end_lending_time, book[0])
                self.repo.update_books_sum(cursor, book[1])
                self.repo.update_status(cursor, book[0])
                if amount_penalty > 0:
                    self.repo.insert_penalty(cursor, person[1], amount_penalty)
                print(f'\nLa persona {person[0]} - CI: {person[1]} tiene una penalizacion de {amount_penalty}$.\n')
                conn.commit()
            except sqlite3.Error as e:
                logging.critical(f'Error en base de datos: {e}')
                conn.rollback()