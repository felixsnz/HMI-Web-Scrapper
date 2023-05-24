import threading
from web.driver import ChromeDriver
from web.scrapper import Scrapper
from sql.record_ingestor import RecordIngestor
from raspberry.modbus_server import ModbusServer

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

hmi_ip_address = config['hmi']['ip']



url = f'http://{hmi_ip_address}/logs/Customs/'

def main():

    # create an instance of FolderWatchdog
    ingestor = RecordIngestor(r"downloads")
    ingestor_thread = threading.Thread(target=ingestor.start)
    ingestor_thread.start()

    # create an instance of ModbusServer
    modbus_server = ModbusServer()

    # run the ModbusServer in a new thread
    modbus_thread = threading.Thread(target=modbus_server.run)
    modbus_thread.start()

    driver = ChromeDriver('/usr/lib/chromium-browser/chromedriver')

    scrapper = Scrapper(url, driver=driver)

    scrapper.run()
    

if __name__ == '__main__':
    main()