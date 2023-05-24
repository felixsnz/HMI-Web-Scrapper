import os
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from manager import DBManager
import configparser

class CsvFileHandler(FileSystemEventHandler):
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith('.csv'):
            return

        df = pd.read_csv(event.src_path)

        if "E_Standard" not in df.columns:
            print(f"Error: 'E_Standard' column not found in file {event.src_path}")
            return

        for _, row in df.iterrows():
            table = row['E_Standard']
            data = row.drop('E_Standard').tolist()
            self.db_manager.insert(table, data)


class RecordIngestor:
    def __init__(self, path):
        self.path = path
        self.db_manager = None
        # Read database configuration
        config = configparser.ConfigParser()
        config.read('config.ini')

        host = config['sql']['host']
        database = config['sql']['database']
        user = config['sql']['user']
        password = config['sql']['password']

        self.db_manager = DBManager(driver='your-driver', server=host,
                                    database=database, user=user, password=password)
        self.db_manager.connect()
        

    def start(self):
        event_handler = CsvFileHandler(self.db_manager)
        observer = Observer()
        observer.schedule(event_handler, self.path, recursive=False)
        observer.start()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

        self.db_manager.disconnect()