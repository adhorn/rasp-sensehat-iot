#!/usr/bin/python3
import ssl
import paho.mqtt.client as mqtt

try:
    from local_settings import ROOT_CA, CERTFILE, KEYFILE, AWS_IOT_ENDPOINT
except ImportError:
    from default_settings import ROOT_CA, CERTFILE, KEYFILE, AWS_IOT_ENDPOINT


def on_connect(mqttc, obj, flags, rc):
    if rc == 0:
        print("Status code: {0} | Connection successful".format(rc))
    elif rc == 1:
        print("Status code: {0} | Connection refused".format(rc))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print(
        "Subscribed: {0} data: {1}".format(mid, granted_qos)
    )


def on_message(mqttc, obj, msg):
    print(
        "Received message from {0} | QoS: {1} | Data: {2}".format(
            msg.topic, msg.qos, msg.payload
        )
    )


mqttc = mqtt.Client(client_id="mqtt-test")

#callbacks
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
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
