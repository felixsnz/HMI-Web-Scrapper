from pymodbus.server.async_io import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import threading
import time

class ModbusServer:
    def __init__(self, coil_address=1, initial_coil_state=True, host="10.13.141.110", port=502):
        self.coil_address = coil_address
        self.initial_coil_state = initial_coil_state
        self.host = host
        self.port = port

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
    
    def toggle_coil(self):
        while True:
            coils = self.store.getValues(1, self.coil_address)

            current_state = self.initial_coil_state
            if len(coils) > 0:
                current_state = self.store.getValues(1, self.coil_address)[0]

            # Write the opposite state to the coil
            self.store.setValues(1, self.coil_address, [not current_state])

            # Wait for 1 second
            time.sleep(15)
            print("toggling:", current_state)
    
    def run(self):
        # Start a new thread that toggles the coil state every second
        toggle_thread = threading.Thread(target=self.toggle_coil)
        toggle_thread.start()

        # Start the Modbus TCP server
        StartTcpServer(context=self.context, identity=self.identity, address=(self.host, self.port))