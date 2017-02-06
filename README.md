# rasp-sensehat-iot
Sending data from Raspberry Pi with Sensehat sensor to IoT


create Data mapping to ES

curl -i -X PUT -d '{
  "mappings": {
    "sensehat": {
      "properties": {
        "datetime": {
          "type": "date",
          "format" : "yyyy-MM-dd HH:mm:ss"
        },
        "device_id": {
          "type": "string"
        },
        "yaw": {
          "type": "double"
        },
        "pitch": {
          "type": "double"
        },
        "roll": {
          "type": "double"
        },
        "pressure": {
          "type": "double"
        },
        "humidity": {
          "type": "double"
        },
        "temperature": {
          "type": "double"
        }
      }
    }
  }
}
' 'https://URL/index'