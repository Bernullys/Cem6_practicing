import sqlite3

database_name = "energy_consumption.db"

connect_db = sqlite3.connect(database_name)
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

def insert_lectures(lectures, sensor_id, time_stamp):
    connect_db = sqlite3.connect(database_name)
    cursor_db = connect_db.cursor()
    lectures.append(sensor_id)
    lectures.append(time_stamp)
    cursor_db.execute( """
    INSERT INTO lectures ( voltage_V, current_A, frecuency_Hz, active_power_W, reactive_power_var, aparent_power_VA, power_factor, active_energy_consumption_kWh, sensor_id, lecture_time)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (lectures))
    connect_db.commit()
    connect_db.close()


def energy_by_id_and_range(sensor_id, start_time, end_time):
    connect_db = sqlite3.connect(database_name)
    cursor_db = connect_db.cursor()
    cursor_db.execute("""
    SELECT MAX(active_energy_consumption_kWh) - MIN(active_energy_consumption_kWh) FROM lectures WHERE sensor_id = ? AND lecture_time BETWEEN ? AND ?
    """, (sensor_id, start_time, end_time))
    energy_consumption = cursor_db.fetchall()
    connect_db.close()
    return energy_consumption
