# coding: utf-8
import subprocess

# ---------------------------------------------------------


# get voltage

string_before_cleaning_and_decoding =  subprocess.Popen("sudo i2cget -y 1 0x62 0x02 w", shell=True, stdout=subprocess.PIPE).stdout
string_before_cleaning = string_before_cleaning_and_decoding.read()

# remove the 0x starting byte
string = string_before_cleaning[2:]
print(string)

# i hate my life
#def swap(str):
#   if len(str) <= 1:
#      return str
#   middle = str[1:len(str) - 1]
#   return str[len(str) - 1] + middle + str[0]

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


# ---------------------------------------------------------


# calculate estimated battery %
# you can remove anything below this. it's not nessesary to get voltage.

# get percent
hex_raw_battery = subprocess.check_output("sudo i2cget -y 1 0x62 0x4 b", shell=True)

#convert to decimal
battery_percent = int(hex_raw_battery, 16)

# output the voltage
print(battery_percent)

