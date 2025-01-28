from pymodbus.client import ModbusSerialClient

# Connecting the cem6 to the usb port using its communication parameters
client = ModbusSerialClient(port="/dev/ttyUSB0", timeout=2, baudrate=9600, bytesize=8, parity="N", stopbits=1)
# Connecting the divice
client.connect()
# Setting into a variable the actual id of the divice
slave_id = 4
rr = client.read_holding_registers(address=0, count=97, slave=slave_id) #97 is the maximun count for this device.

# Closing the connection with the divice
client.close()

# Memory map modbus address in decimal
map_cem6 = {
    "voltage": 0,
    "current": 1,
    "frecuency": 2,
    "active power": 3,
    "reactive power": 4,
    "aparent power": 5,
    "power factor" : 6,
    "total active energy_1": 7,
    "total active energy_2": 8,
    "total reactive energy_1": 17,
    "total reactive energy_2": 18,
    "time_1": 33,
    "time_2": 34,
    "time_3": 35,
    "time_4": 36,
    "baud rate": 42,
    "id": 43,
    "total active energy consumption_1": 45,
    "total active energy consumption_2": 46,
    "total active energy generation_1": 55,
    "total active energy generation_2": 56,
    "total reactive inductive energy consumption_1": 65,
    "total reactive inductive energy consumption_2": 66,
    "total reactive inductive energy generation_1": 75,
    "total reactive inductive energy generation_2": 76,
    "total reactive capacitive energy consumption_1": 85,
    "total reactive capacitive energy consumption_2": 86,
    "total reactive capacitive energy generation_1": 95,
    "total reactive capacitive energy generation_2": 96,
}
# Taking real lectures from divice
for indx, r in enumerate(rr.registers):
    print(f"Index: {indx} Lecture: {r}")