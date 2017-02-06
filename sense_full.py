from sense_hat import SenseHat
from datetime import datetime
import boto3
import time
import json

region = 'eu-west-1'
iot = boto3.client('iot-data', region_name=region)
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
    print acceleration
    print dir(acceleration)
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
    temperature = sense.get_temperature_from_humidity()
    print("Temperature: %s C" % temperature)
    return temperature


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
    payload['timestamp'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    print(payload)
    response = iot.publish(
        topic=topic,
        payload=json.dumps(payload)
    )
    time.sleep(5)
