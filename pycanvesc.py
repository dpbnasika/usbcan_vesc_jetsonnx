#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Description:
    A simple python library to control vesc motor controller from can command packets
    At the time of testing the dependencies for this file to work as expected on Jetson XavierNX is 
    python version: 2.1.17
    python-can module version: 3.3.4
@Note:
    This is also compatible to integrate in ROS1 on Jetson Xavier NX

@Author:
    DP

@TO-DO:
    Implement the other getter functionalities and status message id's

@Example:
    python test_pycanvesc.py
'''

from enum import Enum
import can
import socket
import struct


#CAN Packet ID's
class CANPacketID(Enum):
    CAN_PACKET_SET_DUTY = 0
    CAN_PACKET_SET_CURRENT = 1
    CAN_PACKET_SET_CURRENT_BRAKE = 2
    CAN_PACKET_SET_RPM = 3
    CAN_PACKET_SET_POS = 4


class PyCanVesc:
    
    '''
    Intitialize the can interface bus with the specified values such as
    
    @param: can_interface bus type - ex: socketcan, pcan, ixxat, vector, etc.
    @param: can_channel type - ex: vcan0, can0, PCAN_USBBUS1, etc.
    @param: can_bitrate - ex: 250000,500000, etc.

    ''' 
    def __init__(self,can_interface,can_channel, can_bitrate):
        try:
            self.can_interface = can_interface
            self.can_channel = can_channel
            self.can_bitrate = can_bitrate
            self.bus = can.interface.Bus(interface= can_interface, channel=can_channel, bitrate=can_bitrate)
        except socket.error as e:
            print(e.errno)

    ''' 
    Transmit the motor duty cycle packet to the CAN bus 
    @param: duty_cycle range (0-1) - ex: 0.01
    @param: device_id - vesc can device id
    '''
    def set_motor_duty_cycle(self, duty_cycle, device_id):
        try:
            duty = int(duty_cycle*100000.0)
            data_frame = list()
            data_frame[0:4] = struct.pack(">i",duty)
            print(data_frame)
            message = can.Message(arbitration_id=(CANPacketID.CAN_PACKET_SET_DUTY.value<<8|device_id), data=data_frame, is_extended_id = True)
            print(message)
            self.bus.send(message)
            print("sent duty_cycle can message")
        except can.CanError:
            print("Failed to send the CAN duty cycle Message Frame")

    ''' 
    Transmit the motor position packet to the CAN bus 
    @param: position range (0-360 degrees) - ex: 90
    @param: device_id - vesc can device id
    '''
    def set_motor_pos(self, pos, device_id):
        try:
            position = int(pos*1000000.0)
            data_frame = list()
            data_frame[0:4] = struct.pack(">i",position)
            print(data_frame)
            message = can.Message(arbitration_id=(CANPacketID.CAN_PACKET_SET_POS.value<<8|device_id), data=data_frame, is_extended_id = True)
            print(message)
            self.bus.send(message)
            print("sent position can message")
        except can.CanError:
            print("Failed to send the CAN position Message Frame")
    
    ''' 
    Transmit the motor rpm packet to the CAN bus 
    @param: rpm ex: 1000 check the limit in the vesc app and configure
    @param: device_id - vesc can device id
    '''
    def set_motor_rpm(self, rpm, device_id):
        try:
            rotations = int(rpm)
            data_frame = list()
            data_frame[0:4] = struct.pack(">i",rotations)
            print(data_frame)
            message = can.Message(arbitration_id=(CANPacketID.CAN_PACKET_SET_RPM.value<<8|device_id), data=data_frame, is_extended_id = True)
            print(message)
            self.bus.send(message)
            print("sent rpm can message")
        except can.CanError:
            print("Failed to send the CAN position Message Frame")

