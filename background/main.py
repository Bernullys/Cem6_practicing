from typing import Annotated
from fastapi import FastAPI, BackgroundTasks, Query, Path
from pymodbus.client import ModbusTcpClient
import asyncio
import logging, time

from database_helpers import insert_lectures, energy_by_id_and_range

app = FastAPI()

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

gateway_ip = "192.168.0.100"
gateway_port = 502
cem6_ids = [2, 4]
start_address = 0
last_address = 97
polling_interval = 10

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
                    # Here is where will get store in a database
                    # Here I have to filter the values I want to store in the database
                    lectures = [register for indx, register in enumerate(registers) if indx in electric_parameters]
                    # Datetime value
                    current_time = time.localtime()
                    date_time = time.strftime("%y-%m-%d %H:%M:%S", current_time)
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
    start_add: Annotated[int | None, Query(ge=0, le=97)] = 0, 
    end_add: Annotated[int | None, Query(ge=1, le=97)] = 1
    ):
    """Read specific registers on demand."""
    response = client.read_holding_registers(address=start_add, count=end_add, slave=device_id)

    if response.isError():
        return {f"error of device {device_id}": str(response)}

    return {f"registers of device {device_id}": response.registers}

@app.get("/energy_consumption/{device_id}/")
async def energy_consumption(
    device_id: Annotated[int, Path(ge=1, le=254)],
    start_time: Annotated[str | None, Query(title="this is a title")] = None,
    end_time: Annotated[str, Query()] = None
    ):
    if not start_time or not end_time:
        return {"Energy consumed last month": energy_by_id_and_range(device_id, "25-02-01 00:00:00", "25-02-28 23:59:59")}
    else:
        return {"Energy consumption": energy_by_id_and_range(device_id, start_time, end_time)}