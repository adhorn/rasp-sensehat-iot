Code used during the AWS IoT talk "Derive insights from IoT in minutes on AWS" 

Slides: https://www.slideshare.net/hornsby/derive-insight-from-iot-data-in-minute-with-aws-73773075

**Goal**:
Connect the RaspberryPi with SenseHat to the AWS IoT platform using MQTT protocol and test real-time interaction between the RaspberryPi and the IoT platform.

The mqtt-sub application launches 2 subroutines:
- one publisher sending the data from the temperature sensor of the RaspberryPi Senshat device (publish_topic)
- one subscriber that listened to a topic (subscribe_topic) and that prints out the message received from that topic to the screen of the Sensorhat device.

![Demo](https://github.com/adhorn/rasp-sensehat-iot/blob/master/pics/demo2.png)


**AWS IoT** easily and securely connects devices through the MQTT and HTTPS protocols. The IoT Rules Engine continuously processes incoming messages, enabling your devices to interact with other AWS services.

**MQTT** is a bi-directional protocol [...]

**Prerequisites:**

* Create an IoT "Thing" and download the certificate bundle and unzip the file onto the RaspberryPI. Update the file path of those file in the file ```default_settings.py``` or in a file called ```settings.py````.
Update also the AWS_IOT_ENDPOINT with the endpoint of your IoT "Thing"

* Install the dependencies in ```pip install -r requirements.txt```

* Run the application ```python mqtyt-sub.py```

* In the AWS Console IoT service, select your "Thing" and click "Interact" and "start MQTT"

* Subscribe to the topic "$aws/things/sensehat/shadow/update/temperature" and you should see the temperatures updating from the RaspberryPi.

* Click Publish and select "$aws/things/sensehat/shadow/update/info/test"
(the # is a wildcard) - type any message (e.g Hello Folks!)
You should see in the mqtt-sub.py logging (screen prints) that the RaspberryPi received the message and you should also see that message displayed on the display of the Sensorhat device.
