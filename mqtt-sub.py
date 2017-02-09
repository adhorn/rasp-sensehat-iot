#!/usr/bin/python3
import ssl
import paho.mqtt.client as mqtt

try:
    from local_settings import ROOT_CA, CERTFILE, KEYFILE, AWS_IOT_ENDPOINT
except ImportError:
    from default_settings import ROOT_CA, CERTFILE, KEYFILE, AWS_IOT_ENDPOINT



def on_connect(mqttc, obj, flags, rc):
    if rc == 0:
        print("Status code: {} | Connection successful".format(str(rc)))
    elif rc == 1:
        print("Status code: {} | Connection refused".format(str(rc)))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: {0} {1} data: {2}".format(
        str(mid), str(granted_qos), str(obj)
    ))


#called when a message is received by a topic
def on_message(mqttc, obj, msg):
    print("Received message from {0} | QoS: {1} | Data: {2}".format(
        msg.topic, str(msg.qos), str(msg.payload)
    ))


#creating a client with client-id=mqtt-test
mqttc = mqtt.Client(client_id="mqtt-test")

mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support as required by aws-iot service
mqttc.tls_set(
    ROOT_CA,
    certfile=CERTFILE,
    keyfile=KEYFILE,
    tls_version=ssl.PROTOCOL_TLSv1_2,
    ciphers=None
)

#connecting to aws-account-specific-iot-endpoint
mqttc.connect(AWS_IOT_ENDPOINT, port=8883)

mqttc.subscribe("$aws/things/sensehat/shadow/update/#", qos=1) #The names of these topics start with $aws/things/thingName/shadow."

#automatically handles reconnecting
mqttc.loop_forever()