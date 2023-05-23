from pymodbus.client.sync_diag import ModbusTcpClient

client = ModbusTcpClient('169.254.177.1', port=502)

response = client.read_coils(1, 1)

if response.isError():
    print("Could not read coil: ", response)
else:
    print("Coil value: ", response.bits[0])

client.close()