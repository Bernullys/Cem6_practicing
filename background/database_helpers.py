import sqlite3

# Database name:
database_name = "energy_consumption.db"

# Create/Connect to the database and then create lectures table:
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

# Create users table:
cursor_db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        rut TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL,
        address TEXT NOT NULL,
        sensor_id INTEGER NOT NULL,
        FOREIGN KEY(sensor_id) REFERENCES lectures(sensor_id)
    )
""")

# Create historical lectures table to store the monthly energy consumption on the database, and then to be used as historical for the graphic.
cursor_db.execute(
    """
        CREATE TABLE IF NOT EXISTS historical_lectures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor_id INTEGER NOT NULL,
        month TEXT NOT NULL,
        year TEXT NOT NULL,
        monthly_consumption REAL
    )"""
)
connect_db.commit()
connect_db.close()


# Function to add a user to the database using the User instance and then to be used on post method:
def add_user_to_db(new_user):
    connect_db = sqlite3.connect(database_name)
    cursor_db = connect_db.cursor()
    cursor_db.execute(
        """
        INSERT INTO users (first_name, last_name, rut, phone, email, address, sensor_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (new_user.first_name, new_user.last_name, new_user.rut, new_user.phone, new_user.email, new_user.address, new_user.sensor_id)
    )
    connect_db.commit()
    connect_db.close()
    return {"message": "User added successfully", "user": new_user.dict()}

# Insert values from devices into the database:
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

# Read energy from a device in a selected range of time:
def energy_by_id_and_range(sensor_id, start_time, end_time):
    connect_db = sqlite3.connect(database_name)
    cursor_db = connect_db.cursor()
    cursor_db.execute("""
    SELECT MAX(active_energy_consumption_kWh) - MIN(active_energy_consumption_kWh) FROM lectures WHERE sensor_id = ? AND lecture_time BETWEEN ? AND ?
    """, (sensor_id, start_time, end_time))
    energy_consumption = cursor_db.fetchone()
    connect_db.close()
    return energy_consumption[0]

# Function to add the monthly energy consumption to the historical_lectures table every month:
def add_monthly_consumption_to_db(sensor_id, month, year, monthly_energy_consumption):
    connect_db = sqlite3.connect(database_name)
    cursor_db = connect_db.cursor()
    cursor_db.execute(
        """
        INSERT INTO historical_lectures (sensor_id, month, year, monthly_consumption)
        VALUES (?, ?, ?, ?)
        """, (sensor_id, month, year, monthly_energy_consumption)
    )
    connect_db.commit()
    connect_db.close()

# Funtion to query all the data we need to print the invoice:
async def bring_invoice_data(first_day_previous_month, last_day_previous_month, sensor_id):
    connect_db = sqlite3.connect(database_name)
    cursor_db = connect_db.cursor()
    # Bring data from lectures table:
    cursor_db.execute(
        """"
            SELECT MIN(active_energy_consumption_kWh), MAX(active_energy_consumption_kWh)
            FROM lectures
            WHERE lecture_time BETWEEN ? AND ?
        """,(first_day_previous_month, last_day_previous_month)
    )
    data_from_lectures = cursor_db.fetchone()
    first_month_lecture = data_from_lectures[0]
    last_month_lecture = data_from_lectures[1]
    month_energy_consumption = (float(last_month_lecture) - float(first_month_lecture))/100 # In kWh
    monthly_cost = month_energy_consumption * 123
    # Now bring the info of the customer:
    cursor_db.execute(
        """
            SELECT  sensor_id, first_name, last_name, address
            FROM users
            WHERE sensor_id = ?
        """, (sensor_id,))
    data_from_users = cursor_db.fetchone()
    client_num = data_from_users[0]
    client_first_name = data_from_users[1]
    client_last_name = data_from_users[2]
    client_address = data_from_users[3]
    connect_db.close()
    return [first_month_lecture, last_month_lecture, month_energy_consumption, monthly_cost, client_num, client_first_name, client_last_name, client_address]

