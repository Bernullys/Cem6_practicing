from typing import Annotated, Optional, Dict
from fastapi import FastAPI, BackgroundTasks, Query, Path, HTTPException, Depends, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pymodbus.client import ModbusTcpClient
from pydantic import BaseModel, Field, EmailStr
import asyncio
import logging, time
from datetime import datetime, timedelta
import re
from ping3 import ping, EXCEPTIONS
import platform
from auth import router as auth_router
from auth import get_current_user

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

influx_server_url = "http://localhost:8086"
influx_token = "4Up32I3Xg5xU3X3X5c_T5ksBBolkOxtcn-6VC4d0XpX0kG1Hq90pprEfRShSGOJ_pA70to9jzb8baZp_ISC8yA=="
influx_org = "test"
influx_bucket = "test"

influx_client = InfluxDBClient(url=influx_server_url, token=influx_token, org=influx_org)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)


# Importing functions from database_helpers.py and invoice_pdf_maker.py:
from database_helpers import add_user_to_db, insert_lectures, energy_by_id_and_range, add_monthly_consumption_to_db, bring_invoice_data, get_current_devices
from invoice_pdf_maker import invoice, graph_maker

# Regular expressions for validation on some inputs:
name_pattern = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s'-]{3,50}$")
rut_pattern = re.compile(r"^\d{7,8}-[\dkK]$")
phone_pattern = re.compile(r"^\+?(56)?\d{9}$")
address_pattern = re.compile(r"^[\w\s\.\-#º°/,]{5,100}$")
datetime_pattern = re.compile(r"^(|\d{4}-\d{2}-\d{2}( \d{2}:\d{2}:\d{2})?)$")

# Pydantic BaseModel for users:
class UserCreate(BaseModel):
    first_name: str = Field(..., max_length=50, min_length=3, description="First name of the user", example="Bernardo", pattern=name_pattern)
    last_name: str = Field(..., max_length=50, min_length=3, description="Last name of the user", example="Dávila", pattern=name_pattern)
    rut: str = Field(..., max_length=10, min_length=9, description="RUT of the user", example="12345678-9", pattern=rut_pattern)
    phone: str = Field(..., max_length=12, min_length=9, description="Phone number of the user", example="+56995433938", pattern=phone_pattern)
    email: EmailStr = Field(..., max_length=50, description="Email of the user", example="bernardoantoniod@gmail.com")
    address: str = Field(..., max_length=100, min_length=5, description="Address of the user", example="Av. Libertador Bernardo O'Higgins 1234", pattern=address_pattern)
    sensor_id: int = Field(..., ge=1, le=254, description="Sensor ID of the user", example=2)

# User response model:
class UserResponse(BaseModel):
    message: str
    user: UserCreate

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

# Include the auth router for authentication endpoints:
app.include_router(auth_router)

# Communicate with my frontend / Enable CORS:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:3000"], # Here will be the frontend URL in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging configuration: (Debugging)
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Modbus gateway configuration:
gateway_ip = "192.168.100.100"
gateway_port = 502
cem6_ids = [2, 4, 5]
start_address = 0
last_address = 97
polling_interval = 30
client = ModbusTcpClient(host=gateway_ip, port=gateway_port, timeout=2)

# ------------- Status checking ------------------------------------- #
# Gateway's list:
gateways_list = {
    1: "192.168.100.100",
    2: "192.168.100.15"
}
# Gateway's status:
gateways_status: Dict[int, str] = {}

async def system_ping(ip: str) -> bool:
    param = "-n" if platform.system().lower() == "windows" else "-c"
    proc = await asyncio.create_subprocess_exec(
        "ping", param, "1", ip,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )
    return (await proc.wait()) == 0


async def gateways_monitor():
    while True:
        for gateway_id, ip in gateways_list.items():
            try:    
                is_up = await system_ping(ip)
                
                gateways_status[gateway_id] = "connected" if is_up else "disconnected"
            except Exception as e:
                gateways_status[gateway_id] = "disconnected"
                print(f"Error pinging {ip}: {e}")
        await asyncio.sleep(10)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(gateways_monitor())

@app.get("/device_status/")
async def get_status():
    return gateways_status

@app.websocket("/ws/status/")
async def websocket_status(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(gateways_status)
            await asyncio.sleep(5)
    except Exception as e:
        print(f"WebSocket disconnected: {e}")

# ------------- Status checking ------------------------------------- #


# Flag to run poll_modbus function
running = False

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

# Function to raise an exception if the device is not found in the database:
def raising_by_not_device_on_db (device_id):
    # Checking existin device ids in the database:
    existing_device_ids = get_current_devices()
    if device_id not in existing_device_ids:
        raise HTTPException(
            status_code=404,
            detail = f"Device {device_id} not found in the database."
        )


async def poll_modbus():
    # Continuously read registers and store them in a database
    global running
    while running:
        try:
            if not client.connect():
                logging.warning("Gateway DISCONNECTED")
                client.close()
                await asyncio.sleep(polling_interval)
                continue
            logging.info("Gateway CONNECTED")

            # Read holding registers
            for device_id in cem6_ids:
                response = client.read_holding_registers(address=start_address, count=last_address, slave=device_id)
                if response.isError():
                    logging.error(f"Modbus error for device: {device_id}. Error description: {response}")
                    client.close()
                else:
                    # Defining date and time variables:
                    actual_time_variables = time_variables()
                    # Reding registers from the device:
                    registers = response.registers
                    # logging.info(f"Received Registers from device: {device_id}, registers: {registers}")
                    # Here I have to filter the values I want to store in the database
                    lectures = [register for indx, register in enumerate(registers) if indx in electric_parameters]
                    
                    # New part: Send to InfluxDB to make graphics:
                    voltage_lecture = float(lectures[0])
                    current_leture = float(lectures[1])
                    frecuency_lecture = float(lectures[2])
                    active_power_lecture = float(lectures[3])
                    reactive_power_lecture = float(lectures[4])
                    aparent_power_lecture = float(lectures[5])
                    power_factor_lecture = float(lectures[6])
                    active_energy_lecture = float(lectures[7])
                    try:
                        point = (
                            Point("cem6_readings")
                            .field("voltage", voltage_lecture)
                            .field("current", current_leture)
                            .field("frecuency", frecuency_lecture)
                            .field("active_power", active_power_lecture)
                            .field("reactive_power", reactive_power_lecture)
                            .field("aparent_power", aparent_power_lecture)
                            .field("power_factor", power_factor_lecture)
                            .field("active_energy", active_energy_lecture)
                            .time(datetime.utcnow())
                        )
                        write_api.write(bucket=influx_bucket, org=influx_org, record=point)
                        print(f"Wrote to InfluxDB: {voltage_lecture}")
                    except Exception as e:
                        print(f"Error writting to influxdb: {e}")

                    
                    # Here is where will get store in a database
                    insert_lectures(lectures, device_id, actual_time_variables[1])
                    # Now add the monthly energy consumption to the historical_lectures table:
                    if actual_time_variables[6] == "01" and actual_time_variables[7] == "00" and int(actual_time_variables[8]) <= 15:
                        energy_to_historical_table = energy_by_id_and_range(device_id, actual_time_variables[9], actual_time_variables[10])
                        add_monthly_consumption_to_db(device_id, actual_time_variables[3], actual_time_variables[4], energy_to_historical_table)
                    client.close()
                    
        except Exception as e:
            logging.error(f"Exception in Modbus Polling: {e}")
        await asyncio.sleep(polling_interval)
    client.close()

# Start a background task to run gateways monitor

# Start the background task so the application starts:,
#    current_user: Annotated[dict, Depends(get_current_user)]
@app.get("/start/")
async def start_polling(background_tasks: BackgroundTasks, current_user: Annotated[dict, Depends(get_current_user)]):
    global running
    if not running:
        running = True
        background_tasks.add_task(poll_modbus)
        return {"message": "Modbus polling started"}
    else:
        return {"message": "Modbus polling is not running"}

# Stop the background task so the application stops:
@app.get("/stop/")
async def stop_polling():
    global running
    running = False
    return {"message": "Modbus polling stopped"}

# Add user endpiont:
@app.post("/add_user/", response_model=UserResponse)
async def add_user(new_user: UserCreate):
    return add_user_to_db(new_user)

# Read actual time registers endpoint for a specific device:
@app.get("/read/{device_id}/", response_model=DeviceIdParamResponse)
async def read_register(device_id: Annotated[int, Path(ge=1, le=254)]):
    response = client.read_holding_registers(address=start_address, count=last_address, slave=device_id)

    raising_by_not_device_on_db(device_id)

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
    start_time: Annotated[str | None, Query(pattern=datetime_pattern)] = None,
    end_time: Annotated[str | None, Query(pattern=datetime_pattern)] = None
    ):
    
    raising_by_not_device_on_db(device_id)

    # Defining date and time variables:
    first_day_previous_month = time_variables()[9]
    last_day_previous_month = time_variables()[10]
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
@app.get("/invoice/{device_id}/")
async def print_invoice(device_id: Annotated[int, Path(ge=1, le=254)]):

    raising_by_not_device_on_db(device_id)

    first_day_previous_month = time_variables()[9]
    last_day_previous_month = time_variables()[10]
    try:
        invoice_data = bring_invoice_data(first_day_previous_month, last_day_previous_month, device_id)
        first_month_lecture = invoice_data[0]
        last_month_lecture = invoice_data[1]
        monthly_energy_consumption = invoice_data[2]
        monthly_cost = invoice_data[3]
        client_num = invoice_data[4]
        client_first_name = invoice_data[5]
        client_last_name = invoice_data[6]
        client_address = invoice_data[7]
        graph_maker(device_id, database_name)
        invoice(first_month_lecture, last_month_lecture, monthly_energy_consumption, monthly_cost, first_day_previous_month, last_day_previous_month, time_variables()[1], client_num, client_first_name, client_last_name, client_address)
        return {"message": "Invoice created"}
    except:
        return {"message": "Not data from last month"}





# For the future: I need to create a function that will be called by the background task to create the invoice and send it to the user by email.