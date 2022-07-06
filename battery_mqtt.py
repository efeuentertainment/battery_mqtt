# coding: utf-8
import subprocess
import socket
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


