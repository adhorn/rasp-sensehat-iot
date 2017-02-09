#!/usr/bin/python3
import ssl
import paho.mqtt.client as mqtt

try:
    from local_settings import ROOT_CA, CERTFILE, KEYFILE, AWS_IOT_ENDPOINT
except ImportError:
    from default_settings import ROOT_CA, CERTFILE, KEYFILE, AWS_IOT_ENDPOINT


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


mqttc = mqtt.Client()

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
mqttc.subscribe("$aws/things/sensehat/shadow/update/#", qos=1)
mqttc.loop_forever()
