import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

from background.database_helpers import insert_lectures, energy_by_id_and_range

data_time = time.localtime()
formated_data_time = time.strftime("%y-%m-%d %H:%M:%S", data_time)
#print(formated_data_time)
#print(type(formated_data_time))

list_of_data = [2200, 0, 500]

list_of_data.append(formated_data_time)

#print(list_of_data)

#for ind, l in enumerate(list_of_data):
#    print(ind, l)

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

lectures = [map_cem6["baud rate"], map_cem6["voltage"]]


# leng = 255

# for i in range(leng):
#     if i < leng:
#         print(i)
#     i += 1

# Sample historical data (Months vs. Values)
data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "Value": [100, 120, 90, 150, 130, 160, 170, 180, 140, 155, 165, 175]
}

# Convert to DataFrame
# df = pd.DataFrame(data)

# Plot the data
# plt.figure(figsize=(10, 5))
# plt.plot(df["Month"], df["Value"], marker="o", linestyle="-", color="b", label="Historical Values")

# Customize the graph
# plt.title("Historical Data: Months vs. Values")
# plt.xlabel("Months")
# plt.ylabel("Values")
# plt.grid(True)
# plt.legend()
# plt.savefig("my_graph.png")


# These are the values of addresses (or indexes of registers) of the electrical parameters shown correctly on display.
electric_parameters = [map_cem6["voltage"], map_cem6["current"], map_cem6["frecuency"], map_cem6["active power"], map_cem6["reactive power"], map_cem6["aparent power"], map_cem6["power factor"], map_cem6["total active energy consumption_2"]]

these_list = [0, 1, 2, 3, 4, 5]

values_i_want = list(filter(lambda x: x < 4, these_list))
#print(values_i_want)

full_datetime = datetime.now()
date_time = time.strftime("%Y-%m-%d %H:%M:%S")
date = time.strftime("%x")
month = time.strftime("%B")
year = time.strftime("%Y")
time_stamp = time.strftime("%H:%M:%S")

print(date_time, date, month, year, time_stamp, full_datetime)

first_day_previous_month = (full_datetime.replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
last_day_previous_month = (full_datetime.replace(day=1) - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=0)

print(first_day_previous_month, last_day_previous_month)


print(energy_by_id_and_range(4, "2025-02-21 15:44:04", "2025-02-28 16:08:27"))