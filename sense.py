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


# generate normal heart rate with probability .95
def get_accelerometer():
    data = sense.get_accelerometer()
    print("p: {pitch}, r: {roll}, y: {yaw}".format(**data))
    data['type'] = 'acceleration'
    data['device_id'] = get_raspid()
    data['timestamp'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    return json.dumps(data)

while True:
    time.sleep(5)
    acc = get_accelerometer()
    print(acc)
    response = iot.publish(
        topic=topic,
        payload=acc
    )
