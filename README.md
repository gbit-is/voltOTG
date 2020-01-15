# I'm still working on the documentation 


# voltOTG
Python class to interface with a USB volt meter named voltOTG


# Background
While surfing online I spotted a [15$ volt meter](https://pcsensor.com/android-thermometer/mobile-phone-voltmeter-voltotg.html) called "voltOTG" from china that connects to a smartphone, I thought it sounded fun and ordered it.

When I got it I started playing with it in the android app and saw some potential for use with for example a raspberry pi for logging voltages. So I reversed engineered the usb communications and wrote them up as a python class


# How to use

## Basic

### Automatically connect to the voltOTG reader 
```python
import voltotg
reader = voltotg.voltOTG()
reader.autoConnect()
```

### Manually connect 
```python
import voltotg
reader = voltotg.voltOTG()
reader.connectDevice("/dev/tt...")
```

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

### Execute serial command (basic)
```python
import voltotg
reader = voltotg.voltOTG()
reader.autoConnect()
command = "ReadVersion"
reply = reader.bcom(command)
print(reply)
```

### Execute serial command (With empty reply fail-safe*)
```python
import voltotg
reader = voltotg.voltOTG()
reader.autoConnect()
command = "ReadVersion"
reply = reader.scom(command)
print(reply)
```


## Commands avaivable within voltOTG


| voltOTG command | serial command|Explination |
| -------------   | ------------- | ------------- |
| scom (command)  | N/A           | Executes a serial command, returns the reply, even if empty |
| bcom (command)  | N/A           | Executes a serial command, retries if the reply is empty. Returns the reply or error|
| connectDevice(devicePath) | N/A | Attemps to connect to a specified device |
| findDevice()   | N/A            | Looks for a voltOTG device by matching the VID:PID | 
| autoConnect()  | N/A            | Runs findDevice() and uses the reply to connectDevice() |
| getVersion(none,list,version,name) (1) | ReadVersion | Returns the device version, by default it returns just the version |
| readVolt(none,list,voltage,info,raw) (2) | ReadVolt | Only returns the voltage read by the device by default |
| readScale(none,list,scale,calib,raw) (3) | ReadScale | Only returns the scale value by default |
| setScale(float,int) | SetScale:int,float> | Sets the scale value, whatever that is  |
| readPga() | ReadPga | Returns the PGA, not that I have any idea what it does | 
| setPga(1,2,4,9) | SetPga:int>" | Sets the PGA, which does something I assume | 
| readMode() | ReadMode | Returns the mode version|
| setMode(0,1) | SetMode:int> | Sets the mode, if only I had any idea what the modes are|


(1): getVersion() will return the version number, getVersion(list=True) will provide both version and name, getVersion(name=True) will return the name only, getVersion(version=True) will do the same as providing no argument

(2):readVolt() will return a voltage reading in mV, readVolt(list=True) will provide more info from the command, readVolt(raw=True) will return the raw reply from the device, readVolt(info=True) returns a weird one-off inside-the-code documentation, readVolt("voltage=True") does the same as no arguments,  

(3) readScale() will return the scale value, readScale(list=True) will return a list of scale and calib, readScale(raw=True) will return the raw reply from the device, readScale(calib=True) will return the calib value, readScale(scale=True) does the same as providing no argument

## Commands on device not in voltOTG

Due to me having no idea how to handle consistant data streams the first 2 commands were not implemented in the package, the last one was simply left out since I thought it was a bad idea to implement an automatic Zero-ing function, not sure if I agree with that anymore though ........

| Command | Explination |
| -------| -------------- | 
| SetAutoSend:1> | Activates a command that causes the device to send about 1 volt reading per second until it is told to stop |
| SetAutoSend:0> | Deactivates the AutoSend feature of the device 
| SetZero | Causes the device to take the current reading and set it as the zero point for future reads. "reader.bcom("SetZero") would run this command  |



