#!/usr/bin/env python
#
# File: usb_interface.py
# Author: eXtoxesses
# Date: February 18, 2018
#
# (C) COPYRIGHT eXtoxesses 2018
# Released under the same license as Python 3.6.4

import usb.core
import usb.util
from usb.core import *
import sys
import os
import binascii
import time
import serial
import itertools


import usb.backend.libusb1


def openDevice(vendor=None, product=None):
  if (vendor is None) & (product is None):
    print("[ERROR] Invalid IDs: vendor and device cannot be both None")
    return None
  
  device = usb.core.find(idVendor=vendor, idProduct=product)
  device.reset()
  try:
    for config in device:
      for interface in config:
        if device.is_kernel_driver_active(interface.bInterfaceNumber):
          try:
            device.detach_kernel_driver(interface.bInterfaceNumber)
          except usb.core.USBError as e:
            sys.exit("Could not detach kernel driver from interface({0}): {1}".format(interface.bInterfaceNumber, str(e)))
  except NotImplementedError as e:
    print("[ERROR] Impossible to find 'detach_kernel_driver' function. Device handler is returned without detach it!\n")
  
  device.set_configuration()
  return device


def readExample(dev_handler):
  endpoint = dev_handler[0][(0, 0)][2]
  
  # read a data packet
  data = None
  while True:
    try:
      data = dev_handler.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
      print(data)
    except usb.core.USBError as e:
      print("  except")


# https://stackoverflow.com/questions/12542799/communication-with-the-usb-device-in-python
en11_vendor = 0x04D8
en11_device = 0xF0B1
dev_handler = openDevice(en11_vendor, en11_device)


# for cfg in dev_handler:
#   for intf in cfg:
#     # sys.stdout.write('\t' + str(intf.bInterfaceNumber) + ',' + str(intf.bAlternateSetting) + '\n')
#     for ep in intf:
#       sys.stdout.write('\t\t' + str(ep.bEndpointAddress) + '\n')
#       if ep.bEndpointAddress:
#         try:
#           # dev_handler.write(ep.bEndpointAddress, '1', intf.bInterfaceNumber)
#           dev_handler.write(ep.bEndpointAddress, '1')
#         except Exception:
#           print("\t\terror : dev.write("+str(ep.bEndpointAddress)+", 'test', "+str(intf.bInterfaceNumber)+")")

ep = dev_handler[0][(0, 0)][0]
# print(dev_handler[0][(0, 0)].bInterfaceNumber)

command = []
for i in range(1, 64):
  command.append(49)
print(bytearray(command))

# while True:
#   # dev_handler.write(ep.bEndpointAddress, '1', dev_handler[0][(0, 0)].bInterfaceNumber)
#   try:
#     # print(dev_handler.write(ep.bEndpointAddress, 'test'))
#     print(ep.write(bytearray(command)))
#     break
#   except Exception as e:
#     print(e)
    
# readExample(dev_handler)

# Detach device before exit from the script
usb.util.dispose_resources(dev_handler)
