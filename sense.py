from sense_hat import SenseHat
import datetime
import boto3
import time

iot = boto3.client('iot-data')
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
    data['deviceid'] = get_raspid()
    data['datetime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return data

while True:
    time.sleep(1)
    data = get_accelerometer()
    print(data)
    response = iot.publish(
        topic='/sense/acceleration',
        payload=data
    )
