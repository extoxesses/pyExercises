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
# print(dev_handler)
# exit(0)

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

# print(dev_handler[0][(0, 0)].bInterfaceNumber)

# command = []
# for i in range(1, 64):
#   command.append(49)
# print(bytearray(command))

# ESPULSIONE \x10
# RIAVVIO    \x20\x20

# INTERFACCIA 0 - DIGITALIZZATORE
# COSE STRANE CON IL DIGITALIZZATORE \x40
# DIGITALIZZATORE ON \x50
# DIGITALIZZATORE OFF \x51


# print("Call: ", dev_handler[0][(0, 0)][2].write('\x40\x10'))
dev_handler[0][(0, 0)][2].write('\x51')
dev_handler[0][(0, 0)][2].write('\x40\x40')

while True :
  try:
    endpoint = dev_handler[0][(0, 0)][0]
    print("[0]", dev_handler.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize))
  except Exception as e:
    print("Eth0 not passed!")
    
  try:
    endpoint = dev_handler[0][(0, 0)][1]
    print("[1]", dev_handler.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize))
  except Exception as e:
    print("Eth1 not passed!")

  try:
    endpoint = dev_handler[0][(0, 0)][3]
    print("[3]", dev_handler.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize))
  except Exception as e:
    print("Eth3 not passed!")
    
exit(0)





for i in range(1, 64):
  command = ''
  for j in range(1, 64):
    if i == j:
      command = command + '\x40'
    elif j == 2*i:
      command = command + '\x80'
    elif j == 3*i:
      command = command + '\xFF'
    else:
      command = command + '\x05'
  # command = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
  
  # print("Command: ", command)
  endpoint = dev_handler[0][(0, 0)][2]
  endpoint.write(command)
  print("Call: ", dev_handler.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize))
  # print(dev_handler.write(ep.bEndpointAddress, command, dev_handler[0][(0, 0)].bInterfaceNumber))
  
  try :
    endpoint = dev_handler[0][(0, 0)][0]
    print(dev_handler.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize))
  except Exception as e :
    print("Eth1 not passed!")
    
  try :
    endpoint = dev_handler[0][(0, 0)][1]
    print(dev_handler.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize))
  except Exception as e :
    print("Eth1 not passed!")
  
  try :
    endpoint = dev_handler[0][(0, 0)][3]
    print(dev_handler.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize))
  except Exception as e :
    print("Eth1 not passed!")


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
