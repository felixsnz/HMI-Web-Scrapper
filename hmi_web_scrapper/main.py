from optiview_db.record_ingestor import RecordIngestor
from raspberry.modbus import ModbusServer
from raspberry.ethernet import InterfaceMonitor

from scrapper.event_handlers import EStandardLogEventHandler, RecordLogEventHandler
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

logger = get_logger(__name__)

def main():
    current_file_path = os.path.realpath(__file__)
    parent_directory_path = os.path.dirname(os.path.dirname(current_file_path))
    sg.app_path = parent_directory_path
    #run_bash_script("hmi_web_scrapper/scripts/kill_port_process.sh")

    #create an instance of ModbusServer
    # modbus_server = ModbusServer()
    # modbus_thread = threading.Thread(target=modbus_server.run)
    # modbus_thread.start()
    
    # adpt_monitor = InterfaceMonitor('eth0')
    # thread = threading.Thread(target=adpt_monitor.run)
    # thread.start()
    
    downloads_path = os.path.join(parent_directory_path, r"downloads")
    print(downloads_path)
    # create an instance of FolderWatchdog
    ingestor = RecordIngestor(downloads_path)
    ingestor_thread = threading.Thread(target=ingestor.start)
    ingestor_thread.start()

    #logs_watcher = LogWatcher(RecordLogEventHandler())
    #logs_watcher_thread = threading.Thread(target=logs_watcher.run)
    #logs_watcher_thread.start()

if __name__ == '__main__':
    main()