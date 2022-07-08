# battery_mqtt

script to measure battery voltage and send value to MQTT Broker.

measured using CW2015 fuel gauge chip over I2C.
script is useful for Vigibot Robots.

Thanks to OdorousWo1f for the base script.

MQTT publish topics:  
`<hostname>/Vb`		battery voltage in mV  
`<hostname>/updateID`	incrementing update counter  

Install:  
`sudo apt update`  
`sudo apt install python-paho-mqtt`  
`cd /usr/local/`  
`sudo git clone https://github.com/efeuentertainment/battery_mqtt.git`  
`cd battery_mqtt/`  
`sudo chmod +x battery_mqtt.py`  
`python battery_mqtt.py`  

autostart, add to `/etc/rc.local` above `exit 0`  
`python battery_mqtt.py`  

