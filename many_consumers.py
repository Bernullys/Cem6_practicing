from pymodbus.client import ModbusTcpClient
import time, sqlite3

gateway_ip = "192.168.0.100"
gateway_port = 502

cem6_ids = [2, 4]

start_address = 0
last_address = 97

client = ModbusTcpClient(host=gateway_ip, port=gateway_port, timeout=2)
client.connect()


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


while True:
    # Taking registers of the current time
    current_time = time.localtime()
    data_time = time.strftime("%y-%m-%d %H:%M:%S", current_time)

    # These are the electrical parameters shown on display but reactive energy consumption. Because the lecture is grwon.
    electric_parameters = [map_cem6["voltage"], map_cem6["current"], map_cem6["frecuency"], map_cem6["active power"], map_cem6["reactive power"], map_cem6["aparent power"], map_cem6["power factor"], map_cem6["total active energy consumption_2"]]

    lectures = []
    for id in cem6_ids:
        cem6_lecture = client.read_holding_registers(address=start_address, count=last_address, slave=id)
        lectures.append(id)
        lectures.append(data_time)
        for indx, register in enumerate(cem6_lecture.registers):
            if indx in electric_parameters:
                lectures.append(register)

    # Creating a database
    connect_db = sqlite3.connect("many_cem6.db")
    cursor_db = connect_db.cursor()
    cursor_db.execute("""
        CREATE TABLE IF NOT EXISTS lectures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id INTEGER NOT NULL,
            lecture_time TEXT,
            voltage_V REAL,
            current_A REAL,
            frecuency_Hz REAL,
            active_power_W REAL,
            reactive_power_var REAL,
            aparent_power_VA REAL,
            power_factor REAL,
            active_energy_consumption_kWh REAL
        )"""
    )

    # Inserting the list of values into the database
    cursor_db.execute( """
    INSERT INTO lectures (sensor_id, lecture_time, voltage_V, current_A, frecuency_Hz, active_power_W, reactive_power_var, aparent_power_VA, power_factor, active_energy_consumption_kWh)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (lectures[:10]))
    cursor_db.execute( """
    INSERT INTO lectures (sensor_id, lecture_time, voltage_V, current_A, frecuency_Hz, active_power_W, reactive_power_var, aparent_power_VA, power_factor, active_energy_consumption_kWh)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (lectures[10:]))

    connect_db.commit()
    connect_db.close()

    client.close()

    time.sleep(60)