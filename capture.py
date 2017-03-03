import boto3
import os
from sys import argv
from botocore.exceptions import BotoCoreError, ClientError
import json

from picamera import PiCamera
from time import sleep

camera = PiCamera()

try:
    from local_settings import REGION
except ImportError:
    from default_settings import REGION


colors = [
    ['green', 0, 255, 0],
    ['blue', 255, 0, 0],
    ['red', 0, 0, 255],
    ['purple', 255, 0, 255],
    ['silver', 192, 192, 192]
]


reko = boto3.client('rekognition', region_name=REGION)


def take_photo():
    camera.capture('capture/image.jpg')
    return True


def read_image(filename):
    with open(filename, 'r') as f:
        encoded_image_bytes = f.read()
        return encoded_image_bytes


# Amazon Rekognition label detection
def reko_detect_labels(image_bytes):
    print("Calling Amazon Rekognition: detect_labels")
#   speak("Detecting labels with Amazon Recognition")
    response = reko.detect_labels(
        Image={
            'Bytes': image_bytes
        },
        MaxLabels=8,
        MinConfidence=60
    )
    return response


# rekognition facial detection
def reko_detect_faces(image_bytes):
    print("Calling Amazon Rekognition: detect_faces")
    response = reko.detect_faces(
        Image={
            'Bytes': image_bytes
        },
        Attributes=['ALL']
    )
    print(
        json.dumps(
            response,
            sort_keys=True,
            indent=4
        )
    )
    return response
