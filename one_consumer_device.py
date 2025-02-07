from pymodbus.client import ModbusSerialClient
import sqlite3, time

# Connecting the cem6 to the usb port using its communication parameters
client = ModbusSerialClient(port="/dev/ttyUSB0", timeout=2, baudrate=9600, bytesize=8, parity="N", stopbits=1)
# Connecting the divice
client.connect()
# Setting into a variable the actual id of the divice
slave_id = 4

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

# Infinite loop where is going to be read the registers of the divice
while True:
    # Getting into a variable the registers of the divice. This is a list
    rr = client.read_holding_registers(address=0, count=97, slave=slave_id)

    # Taking registers of the current time
    current_time = time.localtime()
    data_time = time.strftime("%y-%m-%d %H:%M:%S", current_time)

    # These are the electrical parameters shown on display but reactive energy consumption. Because the lecture is grwon.
    electric_parameters = [map_cem6["voltage"], map_cem6["current"], map_cem6["frecuency"], map_cem6["active power"], map_cem6["reactive power"], map_cem6["aparent power"], map_cem6["power factor"], map_cem6["total active energy consumption_2"]]
    lectures = []
    for indx, register in enumerate(rr.registers):
        if indx in electric_parameters:
            lectures.append(register)

    # Adding the current time to the registers of the divice to later been inserted together
    lectures.append(data_time)
    # Adding the sensor_id to the lectures
    lectures.append(slave_id)

    # Creating a database
    connect_db = sqlite3.connect("cem6.db")
    cursor_db = connect_db.cursor()
    cursor_db.execute("""
        CREATE TABLE IF NOT EXISTS lectures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id INTEGER NOT NULL,
            voltage_V REAL,
            current_A REAL,
            frecuency_Hz REAL,
            active_power_W REAL,
            reactive_power_var REAL,
            aparent_power_VA REAL,
            power_factor REAL,
            active_energy_consumption_kWh REAL,
            lecture_time TEXT
        )"""
    )

    # Inserting the list of values into the database
    cursor_db.execute( """
    INSERT INTO lectures (voltage_V, current_A, frecuency_Hz, active_power_W, reactive_power_var, aparent_power_VA, power_factor, active_energy_consumption_kWh, lecture_time, sensor_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (lectures))

    # Commiting and closing the db
    connect_db.commit()
    connect_db.close()

    # Closing the connection with the divice
    client.close()

    # Making a pause at the end of the cicle between lectures
    time.sleep(60)
