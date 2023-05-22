import os
import time
import pandas as pd
from sqlite3 import Error
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from manager import DBManager

class MyHandler(FileSystemEventHandler):
    def __init__(self, db_manager:DBManager, folder_to_watch):
        self.db_manager:DBManager = db_manager
        self.folder_to_watch = folder_to_watch

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path

            if file_path.endswith('.csv'):
                print(f'New .csv file detected: {file_path}')

                data = pd.read_csv(file_path)

                if 'model' not in data.columns:
                    print(f"Error: 'model' column not found in {file_path}")
                    return

                for _, row in data.iterrows():
                    table_name = str(row['model'])
                    columns_to_insert = ['column1', 'column2', 'column3']
                    data_to_insert = [row[col] for col in columns_to_insert if col in data.columns]

                    if not data_to_insert:
                        print(f"No valid columns found in {file_path}")
                        continue

                    self.db_manager.insert(table_name, data_to_insert)

class FolderWatchdog:
    def __init__(self, db_file, folder_to_watch):
        self.db_manager = DBManager(db_file)
        self.folder_to_watch = folder_to_watch
        self.observer = Observer()

    def run(self):
        event_handler = MyHandler(self.db_manager, self.folder_to_watch)
        self.observer.schedule(event_handler, self.folder_to_watch, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            self.observer.stop()
            self.observer.join()
            self.db_manager.disconnect()