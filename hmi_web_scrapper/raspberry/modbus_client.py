from pymodbus.client import ModbusTcpClient
from pymodbus.pdu import ModbusResponse
from raspberry.config import ip_address as raspberry_ip
from utils.logger import get_logger

class ModbusClient:
    def __init__(self, host=raspberry_ip, port=502):
        self.host = host
        self.port = port
        self.client = ModbusTcpClient(self.host, self.port)
        self.logger = get_logger(__name__, self.__class__.__name__)

    def read_coil(self, coil_addr):
        response:ModbusResponse = self.client.read_coils(coil_addr, 1)
        
        if response.isError():
            self.logger.error(f"Error reading coil at address {coil_addr}")
        else:
            return response.bits[0]

    def write_coil(self, coil_addr, value):
        response:ModbusResponse = self.client.write_coil(coil_addr, value)
        if response.isError():
            self.logger.error(f"Error writing coil at address {coil_addr}")