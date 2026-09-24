import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

def main_menu(repo, _lending, _return, _add_book, _lendings_defeateds):
    while True:
        print('1. Pedir libro.')
        print('2. Devolver libro.')
        print('3. Agregar libro.')
        print('4. Historial de préstamos vencidos.')
        print('5. Salir')
        
        try:
            option_menu = int(input(''))
            if 0 < option_menu <= 5:
                pass
            else:
                logging.error('Opcion invalida.')
                continue
        except ValueError:
            logging.error('Dato invalido.')
            continue
        
        match option_menu:
            case 1:
                book_lending = _lending.select_book()
                if book_lending:
                    _lending.transaction(book_lending)
            case 2:
                _return.return_book()
            case 3:
                title, copies, authors = _add_book.info_book()
                _add_book.add_book(title, copies, authors)
            case 4:
                _lendings_defeateds.lendings_defeateds()
            case 5:
                break