import ssl
import paho.mqtt.client as mqtt
from time import sleep
from sense_hat import SenseHat
from capture import take_photo

try:
    from local_settings import ROOT_CA, CERTFILE, KEYFILE, AWS_IOT_ENDPOINT
except ImportError:
    from default_settings import ROOT_CA, CERTFILE, KEYFILE, AWS_IOT_ENDPOINT


sense = SenseHat()
sense.clear()

publish_topic = "$aws/things/sensehat/shadow/update/temperature"
subscribe_topic = "$aws/things/sensehat/shadow/update/info/#"
#  '#' in the topic is a wildcard so any topic behond that wildcard will work


def on_connect(mqttc, obj, flags, rc):
    if rc == 0:
        print("Status code: {0} | Connection successful".format(rc))
    elif rc == 1:
        print("Status code: {0} | Connection refused".format(rc))


def on_message(mqttc, obj, msg):
    print(
        "Received message from {0} | QoS: {1} | Data: {2}".format(
            msg.topic, msg.qos, msg.payload
            )
    )
    #  Take the message payload and prints it on the screem
    #  of the sensehat display
    sense.show_message(msg.payload)
    sense.clear()
    print('message payload:{}'.format(msg.payload))
    if 'take_pic' in msg.payload:
        take_photo()


mqttc = mqtt.Client(client_id="mqtt-test")

#callbacks
mqttc.on_connect = on_connect

mqttc.on_message = on_message

mqttc.tls_set(
    ROOT_CA,
    certfile=CERTFILE,
    keyfile=KEYFILE,
    tls_version=ssl.PROTOCOL_TLSv1_2,
    ciphers=None
)


mqttc.connect(AWS_IOT_ENDPOINT, port=8883)
mqttc.subscribe(subscribe_topic, qos=1)
mqttc.loop_start()

while 1:
    sleep(5)
    temp = "%.2f" % sense.get_temperature()
    mqttc.publish(
        publish_topic, temp, qos=1
    )
    print("msg sent to {0}: temperature {1}".format(publish_topic, temp))
