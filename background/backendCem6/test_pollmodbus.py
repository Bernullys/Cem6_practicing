from typing import Annotated, Optional
from fastapi import FastAPI, BackgroundTasks, Query, Path, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pymodbus.client import ModbusTcpClient
from pydantic import BaseModel, Field, EmailStr
import asyncio
import logging, time
from datetime import datetime, timedelta
import re
from auth import router as auth_router
from auth import get_current_user





# Creating a FastAPI instance:
app = FastAPI()


# Communicate with my frontend / Enable CORS:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173"], # Here will be the frontend URL in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging configuration: (Debugging)
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Modbus gateway configuration:
gateway_ip = "192.168.0.100"
gateway_port = 502
cem6_ids = [2, 4]
start_address = 0
last_address = 97
polling_interval = 60
client = ModbusTcpClient(host=gateway_ip, port=gateway_port, timeout=2)

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
# These are the values of addresses (or indexes of registers) of the electrical parameters shown correctly on display.
electric_parameters = [map_cem6["voltage"], map_cem6["current"], map_cem6["frecuency"], map_cem6["active power"], map_cem6["reactive power"], map_cem6["aparent power"], map_cem6["power factor"], map_cem6["total active energy consumption_2"]]

# Datababase name:
database_name = "energy_consumption.db"

# Flag to control the polling loop
running = True

# Function to return time variables:
# Return a list with this variables and order:
# 0 - full_datetime, 1 - date_time, 2 -date, 3 - month, 4 - year, 5 - time_stamp, 6 - day, 7 - hour, 8 - minute, 9 - first_day_previous_month, 10 - last_day_previous_month
def time_variables():
    full_datetime = datetime.now()
    date_time = time.strftime("%Y-%m-%d %H:%M:%S")
    date = time.strftime("%x")
    month = time.strftime("%B")
    year = time.strftime("%Y")
    time_stamp = time.strftime("%H:%M:%S")
    day = time.strftime("%d")
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    first_day_previous_month = (full_datetime.replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_previous_month = (full_datetime.replace(day=1) - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=0)
    return [full_datetime, date_time, date, month, year, time_stamp, day, hour, minute, first_day_previous_month, last_day_previous_month]



async def poll_modbus():
    running = True
    while running:
        try:
            try:
                if not client.connect():
                    logging.error("Failed to connect to Modbus Gateway")
                    raise Exception
                else:
                    gateway_status = "connected"
                    print(gateway_status)
                    pass
            except Exception:
                return {"Error": "Failed to connect to Gateway"}
            # Read holding registers
            print("Reading")
                    
        except Exception as e:
            logging.error(f"Exception in Modbus Polling: {e}")
            return {"Error": "Exception in Modbus Polling function"}

        await asyncio.sleep(polling_interval)

print(asyncio.run(poll_modbus()))