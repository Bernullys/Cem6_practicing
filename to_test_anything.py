import time

data_time = time.localtime()
formated_data_time = time.strftime("%y-%m-%d %H:%M:%S", data_time)
print(formated_data_time)
print(type(formated_data_time))

list_of_data = [2200, 0, 500]

list_of_data.append(formated_data_time)

print(list_of_data)

for ind, l in enumerate(list_of_data):
    print(ind, l)

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
print(lectures)

leng = 255

for i in range(leng):
    if i < leng:
        print(i)
    i += 1