from pymodbus.client import ModbusSerialClient

# Connecting the cem6 to the usb port using its communication parameters
client = ModbusSerialClient(port="/dev/ttyUSB0", timeout=2, baudrate=9600, bytesize=8, parity="N", stopbits=1)
# Connecting the divice
client.connect()

while True:
    try:
        for i in range(256):
            slave_id = i
            print(slave_id)
            rr = client.read_holding_registers(address=0, count=3, slave=slave_id)
            if rr:
                print(rr.registers)
    except AttributeError:
        print("error")
    pass