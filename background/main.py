from typing import Annotated
from fastapi import FastAPI, BackgroundTasks, Query, Path
from pymodbus.client import ModbusTcpClient
import asyncio
import logging

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
            for id in cem6_ids:
                response = client.read_holding_registers(address=start_address, count=last_address, slave=id)
            if response.isError():
                logging.error(f"Modbus error: {response}")
            else:
                registers = response.registers
                logging.info(f"Received Registers: {registers}")
                # Here is where will get store in a database

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
async def read_register(device_id: Annotated[int, Path(ge=1, le=254)], start_add: Annotated[int | None, Query(ge=0, le=97)] = 0, end_add: Annotated[int | None, Query(ge=1, le=97)] = 1):
    """Read specific registers on demand."""
    response = client.read_holding_registers(address=start_add, count=end_add, slave=device_id)

    if response.isError():
        return {f"error of device {device_id}": str(response)}

    return {f"registers of device {device_id}": response.registers}