import paho.mqtt.client as mqtt
import time

client = mqtt.Client()
client.connect("localhost", 1883, 60)

def publishData(data):
    client.publish("home/cam1", data, qos=0, retain=False)
    #time.sleep(10)

