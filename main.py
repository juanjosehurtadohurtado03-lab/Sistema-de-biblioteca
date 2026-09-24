from database.connect import Connection
from database.repo import SQLite_methods
from services.lending import Lendings
from services.return_book import Return
from services.add_book import Add_Book
from services.lending_defeated import Lendings_Defeateds
from cli import main_menu

if __name__=="__main__":
    connection = Connection()
    repo = SQLite_methods(connection)
    _lending = Lendings(repo)
    _return = Return(repo)
    _add_book  = Add_Book(repo)
    _lendings_defeateds = Lendings_Defeateds(repo)
    
    main_menu(repo, _lending, _return, _add_book, _lendings_defeateds)