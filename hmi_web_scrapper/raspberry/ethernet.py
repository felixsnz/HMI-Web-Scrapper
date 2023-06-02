import time
import subprocess
from raspberry.modbus import ModbusClient
from raspberry.config import ip_address as raspberry_ip
from utils.logger import get_logger

class InterfaceMonitor:

    def __init__(self, name):
        self.name = name
        self.last_status = None
        self.modbus_client = ModbusClient(raspberry_ip)
        self.logger = get_logger(__name__, self.__class__.__name__)

    def get_status(self):
        try:
            output = subprocess.check_output(f"cat /sys/class/net/{self.name}/operstate", shell=True).decode('utf-8').strip()
        except Exception as e:
            self.logger.error(f"Error getting the interface status: {e}")
            return None
        return output

    def run(self):
        while True:
            try:
                status = self.get_status()
                if status != self.last_status:
                    if status == 'up':
                        self.modbus_client.write_coil(0, 1)
                        self.logger.info(f"Ethernet device '{self.name}' is connected")
                    elif status == 'down':
                        self.modbus_client.write_coil(0, 0)
                        self.logger.info(f"Ethernet device '{self.name}' is disconnected")
                    else:
                        self.logger.warn(f"Unknown status for device '{self.name}' : {status}")
                    self.last_status = status
                time.sleep(0.5)
            except:
                continue