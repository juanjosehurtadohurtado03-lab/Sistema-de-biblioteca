from database.repo import SQLite_methods
from models.logistics import Time
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

class Lendings_Defeateds:
    def __init__(self, repo: SQLite_methods):
        self.repo = repo
    
    def lendings_defeateds(self):
        now = Time.time_now()
        limit_lendings_list = self.repo.search_lendings_all()
        if not limit_lendings_list:
            logging.info('No hay pedidos.')
            return
        # limit_lendings_list = (id, limit_lending)
        defeated_lendings_id_days = []
        for dl in limit_lendings_list:
            lending_id = dl[0]
            lending_limit = dl[1]
            penalty_time = Time.time_diference(now, lending_limit)
            if penalty_time:
                days = Time.days_defeated(penalty_time)
                defeated_lendings_id_days.append([lending_id, days])
        
        if not defeated_lendings_id_days:
                    logging.info('No hay pedidos vencidos.')
                    return
        # defeated_lendings = [id, days]
        defeated_lendings_complete = []
        for dl in defeated_lendings_id_days:
            lending_id = dl[0]
            days = dl[1]
            
            lending = self.repo.search_lendings_defeated_with_ID(lending_id)
            # lending = (name, ci, title)
            defeated_lendings_complete.append([lending[0], lending[1], lending[2], days])
        defeated_lendings_complete.sort(key=lambda x: x[3], reverse=True)
        
        for dl in defeated_lendings_complete:
            name = dl[0]
            ci = dl[1]
            title = dl[2]
            days = dl[3]
            print(f'{name} - {ci}: {title}. Days: {days}.')