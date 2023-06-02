import time
import subprocess
from raspberry.modbus_client import ModbusClient
from raspberry.config import ip_address as raspberry_ip
from utils.logger import get_logger

class EthernetMonitor:

    def __init__(self, device):
        self.device = device
        self.last_status = None
        self.modbus_client = ModbusClient(raspberry_ip)
        self.logger = get_logger(__name__)

    def get_ethernet_status(self):
        try:
            output = subprocess.check_output(f"cat /sys/class/net/{self.device}/operstate", shell=True).decode('utf-8').strip()
        except Exception as e:
            self.logger.error(f"Error getting the ethernet status: {e}")
            return None
        return output

    def run(self):
        while True:
            status = self.get_ethernet_status()
            if status != self.last_status:
                if status == 'up':
                    self.modbus_client.write_coil(0, 1)
                    self.logger.info(f"Ethernet device {self.device} is connected")
                elif status == 'down':
                    self.modbus_client.write_coil(0, 0)
                    self.logger.info(f"Ethernet device {self.device} is disconnected")
                else:
                    self.logger.warn(f"Unknown status for device {self.device}: {status}")
                self.last_status = status
            time.sleep(1)