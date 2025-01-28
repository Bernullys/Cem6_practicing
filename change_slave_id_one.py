from pymodbus.client import ModbusSerialClient

client = ModbusSerialClient(port="/dev/ttyUSB0", timeout=2, baudrate=9600, bytesize=8, parity="N", stopbits=1)
client.connect()
#breakpoint()
original_slave_id = 0
rr = client.read_holding_registers(address=0, count=3, slave=original_slave_id)
print(f"Client connected id = {original_slave_id} registers= {rr.registers}")
client.close()
print("Client was closed")

new_slave_id = 4
client = ModbusSerialClient(port="/dev/ttyUSB0", timeout=2, baudrate=9600, bytesize=8, parity="N", stopbits=1)
client.connect()
rr = client.write_registers(address=43, values=[new_slave_id], slave=original_slave_id)
"""
if rr isError():
    print("Error changing slave id")
else:
    print(f"Successfully changed slave id to {new_slave_id}")
client.close()
"""
"""
client = ModbusSerialClient(port="/dev/ttyUSB0", timeout=2, baudrate=9600, bytesize=8, parity="N", stopbits=1)
client.connect()
rr = client.read_holding_registers(address=0, count=1, slave=new_slave_id)
if rr isError():
    print("Error reading with the new slave id")
else:
    print(f"Successfully read using slave id to {new_slave_id}")
client.close()
"""
client.close()
client = ModbusSerialClient(port="/dev/ttyUSB0", timeout=2, baudrate=9600, bytesize=8, parity="N", stopbits=1)
client.connect()
rr = client.read_holding_registers(address=0, count=3, slave=new_slave_id)
print(f"Client connected id = {new_slave_id} registers= {rr.registers}")
client.close()