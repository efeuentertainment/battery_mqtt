# coding: utf-8
import subprocess
import socket
import paho.mqtt.client as mqtt
print(socket.gethostname())

# get voltage
string_before_cleaning_and_decoding =  subprocess.Popen("sudo i2cget -y 1 0x62 0x02 w", shell=True, stdout=subprocess.PIPE).stdout
string_before_cleaning = string_before_cleaning_and_decoding.read()

# remove the 0x starting byte
string = string_before_cleaning[2:]
# print(string)

# convert the reported string to number
number_raw_volts = int(string, 16)

# swap MSB and LSB bytes
number_volts = ((number_raw_volts & 0xFF00) >> 8) | ((number_raw_volts & 0x00FF) << 8)

# multiply decimal
uV_volts = number_volts * 305

# divide to get the voltage
voltage = uV_volts / 1000

# output the voltage
print(voltage)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    publish(socket.gethostname(), voltage, qos=0, retain=False)

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
#def on_message(client, userdata, msg):
#    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
#client.on_message = on_message

client.connect("192.168.1.44", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()

