#!/usr/bin/env python2

import paho.mqtt.client as mqtt
import time
import Adafruit_DHT
from configparser import ConfigParser
import json
import struct
import os

config = ConfigParser(delimiters=('=', ))
config.read(os.path.dirname(os.path.realpath(__file__))+'/config.ini')

sensor_type = config['climate-sensor'].get('type', 'dht22').lower()

if sensor_type == 'dht22':
    sensor = Adafruit_DHT.DHT22
elif sensor_type == 'dht11':
    sensor = Adafruit_DHT.dht11
elif sensor_type == 'am2302':
    sensor = Adafruit_DHT.AM2302
else:
    raise Exception('Supported sensor types: DHT22, DHT11, AM2302')

pin = config['climate-sensor'].get('pin', 10)
topic = config['climate-sensor'].get('topic', 'temperature/dht22')
decim_digits = config['climate-sensor'].getint('decimal_digits', 2)
sleep_time = config['climate-sensor'].getint('interval', 60)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code {}".format(rc))
    return

client = mqtt.Client()
client.on_connect = on_connect
client.connect(config['mqtt'].get('hostname', 'homeassistant'),
               config['mqtt'].getint('port', 1883),
               config['mqtt'].getint('timeout', 60))
client.loop_start()

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    data = {'temperature': round(temperature, decim_digits),
            'humidity': round(humidity, decim_digits)}

    client.publish(topic, json.dumps(data))
