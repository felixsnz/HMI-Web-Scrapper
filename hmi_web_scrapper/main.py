from web.driver import ChromeDriver
from web.scrapper import Scrapper
import threading
from local_db.inserter import FolderWatchdog
from hmi.server import ModbusServer


url = 'http://10.13.141.120/logs/Customs/'

def main():

    # create an instance of FolderWatchdog
    watchdog = FolderWatchdog('my_database.db', '/path/to/your/folder')

    # run the FolderWatchdog in a new thread
    thread = threading.Thread(target=watchdog.run)
    thread.start()

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