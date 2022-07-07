#!/usr/bin/env python
# coding: utf-8
import subprocess
import socket
import paho.mqtt.client as mqtt
import threading

updateID = 0

def measure():
#    threading.Timer(30.0, measure).start()
#    print "start measurement"
    t = threading.Timer(30.0, measure)
    t.daemon = True
    t.start()

    # get voltage
    string_before_cleaning_and_decoding =  subprocess.Popen("sudo i2cget -y 1 0x62 0x02 w", shell=True, stdout=subprocess.PIPE).stdout
    string_before_cleaning = string_before_cleaning_and_decoding.read()

    # cleanup measurement
    string = string_before_cleaning[2:]
    number_raw_volts = int(string, 16)
    number_volts = ((number_raw_volts & 0xFF00) >> 8) | ((number_raw_volts & 0x00FF) << 8)
    uV_volts = number_volts * 305
    voltage = uV_volts / 1000

    #mqtt publish results
    client.publish(str(socket.gethostname()) + "/Vb", payload=voltage, qos=0, retain=False)
    
    global updateID
    updateID += 1
    client.publish(str(socket.gethostname()) + "/updateID", payload=updateID,  qos=0, retain=False)

    # output the voltage
    #print(str(voltage) + "mV")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("test/topic") 

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
#client.on_connect = on_connect
#client.on_message = on_message
client.connect("192.168.1.44", 1883, 60)

#start interval timer thread
measure()
    
while True:
    client.loop()
