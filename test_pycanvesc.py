#!/usr/bin/env python

# import the library
from  pycanvesc import PyCanVesc
import time

busType = 'socketcan'
channelType = 'can0'
bitRate = 500000

vescDeviceID = 43
dutyCycle = 0.02 
rpm = 1500
position = 90

def main():
	try:
		PyCanVescObj = PyCanVesc(busType, channelType, bitRate)
		while(True):
			PyCanVescObj.set_motor_duty_cycle(-1*dutyCycle, vescDeviceID)
			time.sleep(3)
			PyCanVescObj.set_motor_duty_cycle(dutyCycle, vescDeviceID)
			time.sleep(3)
	#press ctrl+c to exit
	except KeyboardInterrupt:
		print("exiting")

if __name__ == "__main__":
    main()
