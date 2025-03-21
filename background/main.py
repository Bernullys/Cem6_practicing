from typing import Annotated
from fastapi import FastAPI, BackgroundTasks, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from pymodbus.client import ModbusTcpClient
from pydantic import BaseModel
import asyncio
import logging, time, sqlite3
from datetime import datetime, timedelta

# Importing functions from database_helpers.py:
from database_helpers import insert_lectures, energy_by_id_and_range

# Defining date and time variables:
full_datetime = datetime.now()
date_time = time.strftime("%Y-%m-%d %H:%M:%S")
date = time.strftime("%x")
month = time.strftime("%B")
year = time.strftime("%Y")
time_stamp = time.strftime("%H:%M:%S")
first_day_previous_month = (full_datetime.replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
last_day_previous_month = (full_datetime.replace(day=1) - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=0)


# Instance of Pydantic BaseModel:
class User(BaseModel):
    first_name: str
    last_name: str
    rut: str
    phone: str
    email: str
    address: str
    sensor_id: int

# Function to add a user to the database using the User instance and then to be used on post method:
def add_user_to_db(new_user: User):
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
polling_interval = 300
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

async def poll_modbus():
    # Continuously read registers and store them in a database
    global running
    while running:
        try:
            if not client.connect():
                logging.error("Failed to connect to Modbus Gateway")
                await asyncio.sleep(polling_interval)
                continue
            # Read holding registers
            for device_id in cem6_ids:
                response = client.read_holding_registers(address=start_address, count=last_address, slave=device_id)
                if response.isError():
                    logging.error(f"Modbus error for device: {device_id}. Error description: {response}")
                else:
                    registers = response.registers
                    logging.info(f"Received Registers from device: {device_id}, registers: {registers}")
                    # Here I have to filter the values I want to store in the database
                    lectures = [register for indx, register in enumerate(registers) if indx in electric_parameters]
                    # Here is where will get store in a database
                    insert_lectures(lectures, device_id, date_time)
        except Exception as e:
            logging.error(f"Exception in Modbus polling: {e}")
        await asyncio.sleep(polling_interval)

@app.get("/start")
async def start_polling(background_tasks: BackgroundTasks):
    """Start the Modbus polling in the background."""
    background_tasks.add_task(poll_modbus)
    return {"message": "Modbus polling started"}

@app.get("/stop")
async def stop_polling():
    """Stop the Modbus polling."""
    global running
    running = False
    return {"message": "Modbus polling stopped"}

@app.get("/read/{device_id}")
async def read_register(
    device_id: Annotated[int, Path(ge=1, le=254)], 
    ):
    """Read specific registers on demand."""
    response = client.read_holding_registers(address=start_address, count=last_address, slave=device_id)
    if response.isError():
        return {f"error of device {device_id}": str(response)}
    registers = response.registers
    lectures = [register for indx, register in enumerate(registers) if indx in electric_parameters]
    return {
        "sensor_id": device_id,
        "datetime": date_time,
        "voltage": lectures[0],
        "current": lectures[1],
        "frecuency": lectures[2],
        "active_power": lectures[3],
        "reactive_power": lectures[4],
        "aparent_power": lectures[5],
        "power_factor": lectures[6],
        "active_energy": lectures[7]
        }

@app.get("/energy_consumption/{device_id}/")
async def energy_consumption(
    device_id: Annotated[int, Path(ge=1, le=254)],
    start_time: Annotated[str | None, Query(title="this is a title")] = None,
    end_time: Annotated[str, Query()] = None
    ):
    if not start_time or not end_time:
        return {"Energy consumed last month": energy_by_id_and_range(device_id, first_day_previous_month, last_day_previous_month)}
    else:
        return {"Energy consumption": energy_by_id_and_range(device_id, start_time, end_time)}

@app.post("/add_user/")
async def add_user(new_user: User):
    return add_user_to_db(new_user)
