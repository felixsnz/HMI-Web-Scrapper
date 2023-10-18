from optiview_db.record_ingestor import RecordIngestor
from optiview_db.host_ping_monitor import HostPingMonitor
from raspberry.modbus import ModbusServer, ModbusClient
from raspberry.ethernet import InterfaceMonitor

from scrapper.watcher import LogWatcher
from utils.logger import get_logger
from utils.threads import StoppableThread
from utils.singleton import Singleton as sg

import os
import time
import threading
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
hmi_ip_address = config['hmi']['ip']
sql_server_hostname = config['sql']['host']

logger = get_logger(__name__)

def main():
    current_file_path = os.path.realpath(__file__)
    parent_directory_path = os.path.dirname(os.path.dirname(current_file_path))
    sg.app_path = parent_directory_path
    
    def handle_connection_loss():
        modbus_client = ModbusClient()
        modbus_client.write_coil(1, 0)
    
    #create an instance of ModbusServer
    modbus_server = ModbusServer()
    modbus_thread = threading.Thread(target=modbus_server.run)
    modbus_thread.start()
    
    time.sleep(5)
    
    #monitor = HostPingMonitor(sql_server_hostname, handle_connection_loss)
    
    downloads_path = os.path.join(parent_directory_path, r"downloads")
    print(downloads_path)
    # create an instance of FolderWatchdog
    ingestor = RecordIngestor(downloads_path)
    ingestor_thread = threading.Thread(target=ingestor.start)
    ingestor_thread.start()
    
    time.sleep(5)
    logs_watcher = LogWatcher()
    logs_watcher_thread = threading.Thread(target=logs_watcher.run)
    logs_watcher_thread.start()

if __name__ == '__main__':
    main()