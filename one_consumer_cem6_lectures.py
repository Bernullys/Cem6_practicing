import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from fpdf import FPDF
from one_consumer_pdf import invoice

# Customer:
client_id = 4

# Store in variables the first and last day of the previous month:
actual_date_time = datetime.now()
actual_date = actual_date_time.strftime("%x")
actual_month = actual_date_time.strftime("%B")
actual_year = actual_date_time.year
first_day_previous_month = (actual_date_time.replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
last_day_previous_month = (actual_date_time.replace(day=1) - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=0)
#print(first_day_previous_month, last_day_previous_month)

# Just to make tests:
first_day_previous_month = "25-02-01 00:00:00"
last_day_previous_month = "25-02-05 23:59:59"

# Connect to the database and get the data:
connecting_database = sqlite3.connect("./cem6.db")
cursor = connecting_database.cursor()
cursor.execute(
    """
        SELECT MIN(active_energy_consumption_kWh), MAX(active_energy_consumption_kWh)
        FROM lectures
        WHERE lecture_time BETWEEN ? AND ?
    """,(first_day_previous_month, last_day_previous_month)
)
data_from_lectures = cursor.fetchone()
first_month_lecture = data_from_lectures[0]
last_month_lecture = data_from_lectures[1]
month_energy_consumption = (float(last_month_lecture) - float(first_month_lecture))/100 # In kWh
monthly_cost = month_energy_consumption * 123

# Bring here the info of the customer to use its variables to print the invoice.
cursor.execute(
    """
        SELECT  sensor_id, first_name, last_name, address
        FROM users
        WHERE sensor_id = ?
""", (client_id,))

data_from_users = cursor.fetchone()
client_num = data_from_users[0]
client_first_name = data_from_users[1]
client_last_name = data_from_users[2]
client_address = data_from_users[3]

# Create and add the monthly energy consumption on a table, to be stored and then to be used as historical for the graphic.
cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS historical_lectures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor_id INTEGER NOT NULL,
        month TEXT NOT NULL,
        year TEXT NOT NULL,
        monthly_consumption REAL
    )"""
)

# Adding values to historical_lectures table:
historical_lectures_values = [client_id, actual_month, actual_year, month_energy_consumption]
cursor.execute (
    """
        INSERT INTO historical_lectures (sensor_id, month, year, monthly_consumption)
        VALUES (?, ?, ?, ?)
    """, (historical_lectures_values)
)


connecting_database.commit()
connecting_database.close()


invoice(first_month_lecture, last_month_lecture, month_energy_consumption, monthly_cost, first_day_previous_month, last_day_previous_month, actual_date, client_num, client_first_name, client_last_name, client_address)