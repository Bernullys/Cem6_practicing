from pymodbus.client import ModbusTcpClient
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

gateway_ip = "192.168.0.100"
gateway_port = 502
cem6_id = 4
start_address = 0
last_address = 3

client = ModbusTcpClient(host=gateway_ip, port=gateway_port, timeout=2)

client.connect()

print("Connectedddd")

cem6_response = client.read_holding_registers(address=start_address, count=last_address, slave=cem6_id)

print(cem6_response.registers)

client.close()