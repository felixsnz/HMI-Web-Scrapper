import threading
from web.driver import ChromeDriver
from web.scrapper import Scrapper
from sql.record_ingestor import RecordIngestor
from raspberry.modbus import ModbusServer
from raspberry.ethernet import InterfaceMonitor
from raspberry.bash import run_bash_script
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

hmi_ip_address = config['hmi']['ip']

url = f'http://{hmi_ip_address}/logs/Customs/'

def main():
    
    run_bash_script("hmi_web_scrapper/scripts/kill_port_process.sh")
    
    
    # create an instance of ModbusServer
    modbus_server = ModbusServer()

    # run the ModbusServer in a new thread
    modbus_thread = threading.Thread(target=modbus_server.run)
    modbus_thread.start()
    
    
    adpt_monitor = InterfaceMonitor('eth0')
    thread = threading.Thread(target=adpt_monitor.run)
    thread.start()
    
    
    
    # create an instance of FolderWatchdog
    # ingestor = RecordIngestor(r"downloads")
    # ingestor_thread = threading.Thread(target=ingestor.start)
    # ingestor_thread.start()

    # driver = ChromeDriver('/usr/lib/chromium-browser/chromedriver')
    # scrapper = Scrapper(url, driver=driver)
    # scrapper.run()

if __name__ == '__main__':
    main()