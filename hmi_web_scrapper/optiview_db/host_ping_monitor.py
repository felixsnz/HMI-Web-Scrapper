import os
import time
from threading import Thread
from raspberry.modbus import ModbusClient

class HostPingMonitor:
    def __init__(self, hostname, callback, ping_interval=5):
        self.hostname = hostname
        self.callback = callback
        self.ping_interval = ping_interval
        self.is_running = True
        self.monitor_thread = Thread(target=self._monitor)
        self.monitor_thread.start()
        self.modbus_client = ModbusClient()

    def _monitor(self):
        while self.is_running:
            response = os.system("ping -c 1 " + self.hostname)
            if response != 0:
                self.callback(self.hostname)
            else:
                self.modbus_client.write_coil(1,1)
            time.sleep(self.ping_interval)

    def stop(self):
        self.is_running = False
        self.monitor_thread.join()