from typing import Annotated
from fastapi import FastAPI, BackgroundTasks, Query, Path, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymodbus.client import ModbusTcpClient
from pydantic import BaseModel
import asyncio
import logging, time
from datetime import datetime, timedelta

# Importing functions from database_helpers.py and invoice_pdf_maker.py:
from database_helpers import add_user_to_db, insert_lectures, energy_by_id_and_range, add_monthly_consumption_to_db, bring_invoice_data, get_current_devices
from invoice_pdf_maker import invoice, graph_maker

# Instance of Pydantic BaseModel:
class User(BaseModel):
    first_name: str
    last_name: str
    rut: str
    phone: str
    email: str
    address: str
    sensor_id: int

# User response model:
class UserResponse(BaseModel):
    message: str
    user: User

# Device ID response model:
class DeviceIdParamResponse(BaseModel):
        sensor_id: int
        datetime: str
        voltage: float
        current: float
        frequency: float
        active_power: float
        reactive_power: float
        aparent_power: float
        power_factor: float
        active_energy: float

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
# logging.basicConfig()
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)

# Modbus gateway configuration:
gateway_ip = "192.168.0.100"
gateway_port = 502
cem6_ids = [2, 4]
start_address = 0
last_address = 97
polling_interval = 900
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
                    # Defining date and time variables:
                    actual_time_variables = time_variables()
                    # Reding registers from the device:
                    registers = response.registers
                    logging.info(f"Received Registers from device: {device_id}, registers: {registers}")
                    # Here I have to filter the values I want to store in the database
                    lectures = [register for indx, register in enumerate(registers) if indx in electric_parameters]
                    # Here is where will get store in a database
                    insert_lectures(lectures, device_id, actual_time_variables[1])
                    # Now add the monthly energy consumption to the historical_lectures table:
                    if actual_time_variables[6] == "01" and actual_time_variables[7] == "00" and int(actual_time_variables[8]) <= 15:
                        energy_to_historical_table = energy_by_id_and_range(device_id, actual_time_variables[9], actual_time_variables[10])
                        add_monthly_consumption_to_db(device_id, actual_time_variables[3], actual_time_variables[4], energy_to_historical_table)
        except Exception as e:
            logging.error(f"Exception in Modbus polling: {e}")
        await asyncio.sleep(polling_interval)

# Start the background task so the application starts:
@app.get("/start")
async def start_polling(background_tasks: BackgroundTasks):
    background_tasks.add_task(poll_modbus)
    return {"message": "Modbus polling started"}

# Stop the background task so the application stops:
@app.get("/stop")
async def stop_polling():
    global running
    running = False
    return {"message": "Modbus polling stopped"}

# Add user endpiont:
@app.post("/add_user/", response_model=UserResponse)
async def add_user(new_user: User):
    return add_user_to_db(new_user)

# Read actual time registers endpoint for a specific device:
@app.get("/read/{device_id}", response_model=DeviceIdParamResponse)
async def read_register(device_id: Annotated[int, Path(ge=1, le=254)]):
    response = client.read_holding_registers(address=start_address, count=last_address, slave=device_id)
    # Checking existin device ids in the database:
    device_ids = get_current_devices()
    if device_id not in device_ids:
        raise HTTPException(
            status_code=422,
            detail=f"Device {device_id} not found in the database."
        )
    if response.isError():
        raise HTTPException(
            status_code=502,
            detail=f"Error of device {device_id}, did not respond. Error:{response}"
        )
    # Defining the response list:
    registers = response.registers
    lectures = [register for indx, register in enumerate(registers) if indx in electric_parameters]
    return {
        "sensor_id": device_id,
        "datetime": time_variables()[1],
        "voltage": lectures[0],
        "current": lectures[1],
        "frequency": lectures[2],
        "active_power": lectures[3],
        "reactive_power": lectures[4],
        "aparent_power": lectures[5],
        "power_factor": lectures[6],
        "active_energy": lectures[7]
    }

# Read energy consumption endpoint for a specific device by range or last month by default:
@app.get("/energy_consumption/{device_id}/")
async def energy_consumption_by_range(
    device_id: Annotated[int, Path(ge=1, le=254)],
    start_time: Annotated[str | None, Query()] = None,
    end_time: Annotated[str | None, Query()] = None
    ):
    # Defining date and time variables:
    actual_time_variables = time_variables()
    first_day_previous_month = actual_time_variables[9]
    last_day_previous_month = actual_time_variables[10]
    if (start_time == "") and (end_time == ""):
        return {
            "energy": energy_by_id_and_range(device_id, first_day_previous_month, last_day_previous_month),
            "from": first_day_previous_month,
            "to": last_day_previous_month
            }
    return {
        "energy": energy_by_id_and_range(device_id, start_time, end_time),
        "from": start_time,
        "to": end_time
        }

# Create a PDF invoice for a specific user.
@app.get("/invoice/{sensor_id}")
async def print_invoice(sensor_id: int):
    actual_time_variables = time_variables()
    first_day_previous_month = actual_time_variables[9]
    last_day_previous_month = actual_time_variables[10]
    invoice_data = bring_invoice_data(first_day_previous_month, last_day_previous_month, sensor_id)
    first_month_lecture = invoice_data[0]
    last_month_lecture = invoice_data[1]
    monthly_energy_consumption = invoice_data[2]
    monthly_cost = invoice_data[3]
    client_num = invoice_data[4]
    client_first_name = invoice_data[5]
    client_last_name = invoice_data[6]
    client_address = invoice_data[7]
    graph_maker(sensor_id, database_name)
    invoice(first_month_lecture, last_month_lecture, monthly_energy_consumption, monthly_cost, first_day_previous_month, last_day_previous_month, actual_time_variables[1], client_num, client_first_name, client_last_name, client_address)
    return {"message": "Invoice created"}


# For the future: I need to create a function that will be called by the background task to create the invoice and send it to the user by email.