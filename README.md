# rasp-sensehat-iot
Code used during my walk-through AWS IoT talk at the AWS Meetup Finland "Derive insights from IoT in minutes on AWS"
https://www.meetup.com/awsfin/events/237185018/

Goal:
Get data from RaspberryPi with SenseHat sensor analysed in seconds on the AWS Cloud.


![Demo](https://github.com/adhorn/rasp-sensehat-iot/blob/master/pics/demo.png)


AWS IoT easily and securely connects devices through the MQTT and HTTPS protocols. The IoT Rules Engine continuously processes incoming messages, enabling your devices to interact with other AWS services.

Amazon S3 is object storage that provides you a highly reliable, secure, and scalable storage for all your data, big or small. It is designed to deliver 99.999999999% durability, and scale past trillions of objects.

Amazon Kinesis Firehose allows you to capture and automatically load streaming data into Amazon Kinesis Analytics, Amazon S3, Amazon Redshift, and Amazon Elasticsearch Service, enabling near-real-time business intelligence and the use of dashboards.

Amazon Athena is an interactive query service that makes it easy to analyze data in Amazon S3 using SQL. Simply point to your data in Amazon S3, define the schema, and start querying using standard SQL, with most results delivered in seconds.

Amazon QuickSight is a fast, cloud-powered business analytics service that makes it easy to build visualizations, perform ad-hoc analysis, and quickly get business insights from your data. You can easily run SQL queries using Athena on data stored in S3, and build business dashboards within QuickSight.

Prerequisites:
1. Create an Amazon Kinesis Firehose Stream with the following configuration: 
```
  Delivery stream name: Rasp-SenseHat
  S3 bucket: mys3bucketname
  S3 prefix: raw (or anything else)
  IAM role: firehose_delivery_role (default)
  Data transformation: Disabled
  Source record backup: Disabled
  S3 buffer size (MB): 5
  S3 buffer interval (sec): 60
  S3 Compression: UNCOMPRESSED
  S3 Encryption: No Encryption
  Status: ACTIVE
  Error logging: Enabled
```

2. Create Amazon Elasticsearch Cluster (I used version 2.3) and create security policy to allow access from your IP address only.

3. Create an AWS IoT Rule with the following configuration: 
```
  Rule query statement: SELECT * FROM '<ID_of_the_RaspPI>/sensehat/data'
```

4. Add 2 filters to the AWS IoT Rule:
   * Amazon Kinesis Firehose
```
  Stream name Rasp-SenseHat
  Separator \n (newline)
```
   * Amazon Elasticsearch Service
```
  Domain name yourESdomain
  Endpoint https://yourESdomain.es.amazonaws.com
  ID ${newuuid()}
  Index sensehat
  Type mydata (or anything else)
```

  * create Data mapping to Amazon Elasticsearch with the following configuration:
```
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


5. Configuring Amazon Athena:

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

6. Analysing the data in Amazon Quicksight via Amazon Athena:
  * Create a data source in QuickSight with the following:
```
Log into QuickSight
Select Manage data and New data set.
Choose Athena as a new data source.
Select the default schema and the sensehat_iot_full table created previously in Amazon Athena.
Click Vizualise - Enjoy :)
```

7. Connect into Kibana endpoint found from the Amazon Elasticsearch Service and create an index in setting:
```
Index seach pattern: sensehat*
Select datetime
Vizualise - Enjoy :)
```



