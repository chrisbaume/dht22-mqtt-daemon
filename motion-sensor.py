import paho.mqtt.client as mqtt
from configparser import ConfigParser
import RPi.GPIO as GPIO
import time
import os

config = ConfigParser(delimiters=('=', ))
config.read(os.path.dirname(os.path.realpath(__file__))+'/config.ini')

pin = config['motion-sensor'].getint('pin', 10)
topic = config['motion-sensor'].get('topic', 'motion/sensor')
hostname = config['mqtt'].get('hostname', 'homeassistant')
port = config['mqtt'].getint('port', 1883)
timeout = config['mqtt'].getint('timeout', 60)

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code {}".format(rc))
    return

client = mqtt.Client()
client.on_connect = on_connect
client.connect(hostname,port,timeout)
client.loop_start()

def MOTION(pin):
    client.publish(topic,'motion')

try:
    GPIO.add_event_detect(pin, GPIO.RISING, callback=MOTION)
    while 1:
        time.sleep(100)
except KeyboardInterrupt:
    print 'Quit'
    GPIO.cleanup()
