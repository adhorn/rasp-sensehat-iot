from sense_hat import SenseHat
from datetime import datetime
import boto3
import time
import json
import subprocess

try:
    from local_settings import REGION
except ImportError:
    from default_settings import REGION

iot = boto3.client('iot-data', region_name=REGION)
sense = SenseHat()


def get_raspid():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
    return cpuserial

sensor_id = get_raspid()
delay_s = 60
topic = sensor_id + '/sensehat/data'


# get the data from the accelerometer
def get_accelerometer():
    acceleration = sense.get_accelerometer()
    print("Pitch: {pitch}, Roll: {roll}, Yaw: {yaw}".format(
        **acceleration
        )
    )
    return acceleration


def get_humidity():
    humidity = sense.get_humidity()
    print("Humidity: %s %%rH" % humidity)
    return humidity


def get_temperature():
    # temperature = sense.get_temperature_from_humidity()
    # print("Temperature: %s C" % temperature)
    # Read the sensors
    temp_c = sense.get_temperature()
    cpu_temp = subprocess.check_output("vcgencmd measure_temp", shell=True)
    array = cpu_temp.split("=")
    array2 = array[1].split("'")

    cpu_tempf = float(array2[0]) * 9.0 / 5.0 + 32.0
    cpu_tempf = float("{0:.2f}".format(cpu_tempf))
    # Format the data
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    temp_f = float("{0:.2f}".format(temp_f))
    temp_c = float("{0:.2f}".format(temp_c))
    return temp_c




def get_pressure():
    pressure = sense.get_pressure()
    print("Pressure: %s Millibars" % pressure)
    return pressure


while True:
    payload = get_accelerometer()
    payload['humidity'] = get_humidity()
    payload['temperature'] = get_temperature()
    payload['pressure'] = get_pressure()
    payload['device_id'] = get_raspid()
    payload['datetime'] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(payload)
    response = iot.publish(
        topic=topic,
        payload=json.dumps(payload)
    )
    time.sleep(5)
