from pymodbus.server.async_io import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import threading
import time

from raspberry.config import ip_address as raspberry_ip
from utils.logger import get_logger

class ModbusServer:
    def __init__(self, coil_address=0, initial_coil_state=True, host=raspberry_ip, port=502):
        self.coil_address = coil_address
        self.initial_coil_state = initial_coil_state
        self.host = host
        self.port = port
        self.logger = get_logger(__name__)

        # Create a datastore and initialize it with a coil at address 000001 set to False
        self.store = ModbusSlaveContext(
            co=ModbusSequentialDataBlock(self.coil_address, [self.initial_coil_state])
        )
        self.context = ModbusServerContext(slaves=self.store, single=True)

        # Create a Modbus device identification
        self.identity = ModbusDeviceIdentification()
        self.identity.VendorName = 'Pymodbus'
        self.identity.ProductCode = 'PM'
        self.identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
        self.identity.ProductName = 'Pymodbus Server'
        self.identity.ModelName = 'Pymodbus Server'
        self.identity.MajorMinorRevision = '1.0'
    
    def setup(self):
        # Write the initial state to the coil
        
        self.store.setValues(1, self.coil_address, [self.initial_coil_state])

    
    def run(self):
        setup_thread = threading.Thread(target=self.setup)
        setup_thread.start()

        while True:
            try:
                self.server = StartTcpServer(context=self.context, identity=self.identity, address=(self.host, self.port))
            except OSError as e:
                self.logger.error("OSError occurred, retrying after 3 seconds... Error: {e}")
                time.sleep(3)
                continue
            break