import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from fpdf import FPDF
from one_consumer_pdf import invoice

# Store in variables the first and last day of the previous month:
actual_time = datetime.now()
first_day_previous_month = (actual_time.replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
last_day_previous_month = (actual_time.replace(day=1) - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=0)
#print(first_day_previous_month, last_day_previous_month)

# Just to make tests:
example_start = "25-02-05 13:55:51"
example_end = "25-02-05 14:01:15"

# Connect to the database and get the data:
connecting_database = sqlite3.connect("./cem6_display_lectures.db")
cursor = connecting_database.cursor()
cursor.execute(
    """
        SELECT MIN(active_energy_consumption_kWh), MAX(active_energy_consumption_kWh), MAX(active_power_W)
        FROM lectures
        WHERE lecture_time BETWEEN ? AND ?
    """,(example_start, example_end)
)
cursor.execute(
    """
        SELECT first_name
        FROM users
        WHERE sensor_id = ?
""", ('4',))

data = cursor.fetchone()
first_month_lecture = data[0]
last_month_lecture = data[1]
max_demand = data[2]/1000   # In kW
month_energy_consumption = (last_month_lecture - first_month_lecture)/100 # In kWh
monthly_cost = month_energy_consumption * 123
print(month_energy_consumption, max_demand)
connecting_database.close()


invoice(first_month_lecture, last_month_lecture, month_energy_consumption, monthly_cost, first_day_previous_month, last_day_previous_month, actual_time, client_num, client_name, client_rut, client_address)