import ftplib
import configparser
import os
import time

from optiview_db.manager import DbManager
from optiview_db.config import host, database, user, password
from utils.logger import get_logger

config = configparser.ConfigParser()
config.read('/home/felix/projects/hmi_web_scrapper/config.ini')

hmi_ip_address = config['hmi']['ip']
hmi_user = config['hmi']['user']
hmi_password = config['hmi']['password']

class LogWatcher:
    def __init__(self):
        self.csv_files = []
        self.logger = get_logger(__name__)
        
        
    def connect_ftp(self):
        try:
            self.ftp = ftplib.FTP(hmi_ip_address)
            self.ftp.login(hmi_user, hmi_password)
            self.ftp.cwd("logs")
            #self.logger.info("Successfully connected to FTP.")
        except Exception as e:
            self.logger.error(f"Failed to connect to FTP: {e}")

    def disconnect_ftp(self):
        try:
            self.ftp.quit()
            #self.logger.info("Disconnected from FTP.")
        except Exception as e:
            self.logger.error(f"Failed to disconnect from FTP: {e}")

    def handle_list(self, line):
        line_parts = line.split(maxsplit=8)
        filename = line_parts[-1]
        if filename.lower().endswith('.csv'):
            self.csv_files.append(filename)
            
            #self.logger.info(f"Found CSV file: {filename}")

    def download_file(self, folder_name, filename):
        #self.logger.info(f"downloading file.... {filename}")
        local_dir = os.path.join("/home/felix/projects/hmi_web_scrapper/downloads", folder_name)
        # Check if directory exists before downloading, create it if it doesn't
        if not os.path.isdir(local_dir):
            os.makedirs(local_dir, exist_ok=True)

        local_filename = os.path.join(local_dir, filename)
        #self.logger.info(f"local unexpected local file: {local_filename}")
        if not os.path.isfile(local_filename):  # only download if not exist locally
            try:
                with open(local_filename, 'wb') as f:
                    self.ftp.retrbinary('RETR ' + filename, f.write)
                    #self.logger.info(f"Downloaded and saved file {filename}")
            except Exception as e:
                self.logger.error(f"Failed to download file {filename}: {e}")
        
    def run(self):
        while True:
            try:
                self.connect_ftp()
                db_manager = DbManager(host, database, user, password)
                db_manager.connect()
                folder_list = db_manager.get_table_names()
                for folder_name in folder_list:
                    print("moving to", f"logs/{folder_name}")
                    self.ftp.cwd(f"/logs/{folder_name}")
                    self.csv_files = []
                    self.ftp.retrlines('LIST', self.handle_list)
                    for filename in self.csv_files:
                        self.download_file(folder_name, filename)
                    self.ftp.cwd("..")
                self.disconnect_ftp()
                db_manager.disconnect()
                time.sleep(3)  # Adjust this delay to fit your needs.
            except Exception as e:
                self.logger.error(f"An error occurred in run loop: {e}")
                time.sleep(5)  # If an error occurs, wait before trying again.
                continue