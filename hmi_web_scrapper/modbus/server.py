from pymodbus.server.async_io import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import threading
import time

initial_coil_state = True
coil_address = 1
# Create a datastore and initialize it with a coil at address 000001 set to False
store = ModbusSlaveContext(
    co=ModbusSequentialDataBlock(coil_address, [initial_coil_state])
    
)

context = ModbusServerContext(slaves=store, single=True)

# Create a Modbus device identification
identity = ModbusDeviceIdentification()
identity.VendorName = 'Pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
identity.ProductName = 'Pymodbus Server'
identity.ModelName = 'Pymodbus Server'
identity.MajorMinorRevision = '1.0'

def toggle_coil():
    while True:
        coils = store.getValues(1, coil_address)

        current_state = initial_coil_state
        if len(coils) > 0:
            current_state = store.getValues(1, coil_address)[0]

            
        # Write the opposite state to the coil
        store.setValues(1, coil_address, [not current_state])

        # Wait for 1 second
        time.sleep(15)
        print("toggling:", current_state)

        
        

# Start a new thread that toggles the coil state every second
toggle_thread = threading.Thread(target=toggle_coil)
toggle_thread.start()



# Start the Modbus TCP server
StartTcpServer(context=context, identity=identity, address=("10.13.141.110", 502))