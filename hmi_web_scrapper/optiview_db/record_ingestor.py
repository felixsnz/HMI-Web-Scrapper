import pandas as pd
import os
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from optiview_db.manager import DbManager
from optiview_db import api as optiview_db_api

from optiview_db.config import host, database, user, password

from utils.logger import get_logger

class CsvFileHandler(FileSystemEventHandler):
    def __init__(self, db_manager):
        self.db_manager:DbManager = db_manager
        self.logger = get_logger(__name__, self.__class__.__name__)

    def on_created(self, event:FileSystemEvent):
        if event.is_directory:
            self.logger.warn(f"Directory created: {event.src_path}")
        if not event.src_path.lower().endswith('.csv'):
            self.logger.warn(f"Unexpected file type: {event.src_path}")

        try:
            df = pd.read_csv(event.src_path)
        except Exception as e:
            self.logger.error(f"Couldn't read new file: '{event.src_path}'")
            
            
        subfolder_name = os.path.basename(os.path.dirname(event.src_path))
        self.logger.debug(f"model name: {subfolder_name}")
            

        if not df is None:
            for _, row in df.iterrows():
                data = []
                try:
                    table = subfolder_name
                    serial = row[f'{table}.SerialNumber']
                    uploaded_serials = optiview_db_api.get_serials(table)

                    if serial in uploaded_serials:
                        self.logger.warn(f"there is already a record for the serial: {serial}")
                        return
                    date= row.pop("Date")
                    time = row.pop("Time")

                    timestamp = datetime.strptime(f"{date} {time}", "%Y/%m/%d %H:%M:%S")
                    row_list = row.drop(f'{table}.E_StandardType').tolist()
                    data = [timestamp] + row_list
                    
                    mapping = {'PASS': True, 'FAIL': False}

                    mapped_list = [mapping.get(item, item) for item in data]
                    self.db_manager.insert(table, mapped_list)
                except Exception as e:
                    self.logger.error(f"Error while inserting csv data: {e}")
                finally:
                    self.logger.debug(f"data: {data} inserted at {host}:{database}:{table}")
                    self.logger.debug(f"{self.db_manager._get_column_names(table)}")
        else:
            self.logger.error("there is no df, couldnt load file")



class RecordIngestor:
    def __init__(self, path):
        self.path = path

        self.db_manager = DbManager(
            server=host,
            database=database,
            user=user,
            password=password
        )
        
        self.db_manager.connect()
        

    def start(self):
        #self.logger.info("starting...")
        event_handler = CsvFileHandler(self.db_manager)
        observer = Observer()
        observer.schedule(event_handler, self.path, recursive=True)
        observer.start()

        try:
            while True:
                #TODO trigger event to stop ingestor
                pass
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

        self.db_manager.disconnect()