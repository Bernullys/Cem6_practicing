from pymodbus.client import ModbusTcpClient
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

gateway_ip = "192.168.50.105"
gateway_port = 502
cem6_id_4 = 201
#cem6_id_2 = 2

start_address = 4096
last_address = 124

client = ModbusTcpClient(host=gateway_ip, port=gateway_port, timeout=5)

client.connect()

print("Connectedddd")

cem6_4_response = client.read_holding_registers(address=start_address, count=last_address, slave=cem6_id_4)
#cem6_2_response = client.read_holding_registers(address=start_address, count=last_address, slave=cem6_id_2)

print(cem6_4_response.registers)
print()
#print(cem6_2_response.registers)

client.close()