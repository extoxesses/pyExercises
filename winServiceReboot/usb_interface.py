#!/usr/bin/env python
#
# File: usb_interface.py
# Author: eXtoxesses
# Date: February 18, 2018
#
# (C) COPYRIGHT eXtoxesses 2018
# Released under the same license as Python 3.6.4

import sys
import usb
import usb.backend.libusb1
import time
import usb1

# https://stackoverflow.com/questions/12542799/communication-with-the-usb-device-in-python

device = usb.core.find(idVendor=0x1D57)

# use the first/default configuration
device.set_configuration()
print(device[0][(0, 0)][0])
print(device[0][(1, 0)][0])
print(device[0][(2, 0)][0])

# first endpoint
endpoint = device[0][(1, 0)][0]

# read a data packet
data = None
while True:
  try:
    print("Trying to read")
    data = device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
    print(data)

  except usb.core.USBError as e:
    print("  except")


# handle = usb1.USBContext().openByVendorIDAndProductID(0x1D57, 0xFA60, skip_on_error=True,)
#
# print(handle)
# print("<--->")
# print(device)
# print("<--->")
# print(endpoint)
#
# if handle is None:
#   exit(0)
#   # Device not present, or user is not allowed to access device.
# # with handle.claimInterface(INTERFACE):
#   # Do stuff with endpoints on claimed interface.
#
# while True:
#   data = handle.bulkRead(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
#   print(data)