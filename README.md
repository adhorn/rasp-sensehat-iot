# rasp-sensehat-iot
Code used during my walk-through AWS IoT talk at the AWS Meetup Finland "Derive insights from IoT in minutes on AWS"
https://www.meetup.com/awsfin/events/237185018/

Goal:
Get data from RaspberryPi with SenseHat sensor analysed in seconds on the AWS Cloud.


![Demo](https://github.com/adhorn/rasp-sensehat-iot/pics/demo.png)


create Data mapping to ES
-------------------------
```json
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
```

Athena
-------
```sql
CREATE EXTERNAL TABLE sensehat_iot_full (
    datetime timestamp,
    device_id string,
    yaw double,
    pitch double,
    roll double,
    pressure double,
    temperature double,
    humidity double
  )
ROW FORMAT  serde 'org.apache.hive.hcatalog.data.JsonSerDe'
with serdeproperties( 'ignore.malformed.json' = 'true' )
LOCATION 's3://<BUCKET_NAME>/'
```

