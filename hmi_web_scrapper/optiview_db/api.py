from optiview_db.manager import DbManager
from optiview_db.config import host, database, user, password

def get_serials(table_name):
    db_manager = DbManager(host, database, user, password)
    db_manager.connect()
    values = db_manager.get_column_values(table_name, f'[{table_name}.SerialNumber]')  # If condition is needed
    db_manager.disconnect
    return values