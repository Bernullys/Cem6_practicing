from pymodbus.client import ModbusTcpClient


gateway_ip = "192.168.100.10"
gateway_port = 502
cem6_ids = [1]

start_address = 0
last_address = 3

client = ModbusTcpClient(host=gateway_ip, port=gateway_port, timeout=2)

client.connect()

print("Connectedddd")
lectures = []
for id in cem6_ids:
    lecture = client.read_holding_registers(address=start_address, count=last_address, slave=id)
    lectures.append(lecture.registers)

for lecture in lectures:
    print(lecture)

client.close()