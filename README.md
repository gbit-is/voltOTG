# I'm still working on the documentation 


# voltOTG
Python class to interface with a USB volt meter named voltOTG


# Background
While surfing online I spotted a [15$ volt meter](https://pcsensor.com/android-thermometer/mobile-phone-voltmeter-voltotg.html) called "voltOTG" from china that connects to a smartphone, I thought it sounded fun and ordered it.

When I got it I started playing with it in the android app and saw some potential for use with for example a raspberry pi for logging voltages. So I reversed engineered the usb communications and wrote them up as a python class


# How to use

## Basic

### Reading and printing the voltage every 10 seconds 
```python
import voltotg
from time import sleep
reader = voltotg.voltOTG()
reader.autoConnect()

while True:
  volts = reader.reatVolt()
  print(volts)
  sleep(10)
```
