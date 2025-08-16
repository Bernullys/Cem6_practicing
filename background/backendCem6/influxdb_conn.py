from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import random, time

# Set up your variables
url = "http://localhost:8086"
token = "4Up32I3Xg5xU3X3X5c_T5ksBBolkOxtcn-6VC4d0XpX0kG1Hq90pprEfRShSGOJ_pA70to9jzb8baZp_ISC8yA=="
org = "test"
bucket = "test"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

while True:
    power = round(random.uniform(100, 500), 2)  # Simulated sensor value
    point = Point("power_readings").field("power", power)
    write_api.write(bucket=bucket, org=org, record=point)
    print(f"Written: {power}W")
    time.sleep(5)
