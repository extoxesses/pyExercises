#!/usr/bin/env python
#
# File: usb_interface.py
# Author: eXtoxesses
# Date: February 18, 2018
#
# (C) COPYRIGHT eXtoxesses 2018
# Released under the same license as Python 3.6.4

import usb_utils

# https://stackoverflow.com/questions/12542799/communication-with-the-usb-device-in-python
dev_handler = usb_utils.openDevice(usb_utils.VENDOR_ID, usb_utils.DEVICE_ID)
in_endpoint = dev_handler[0][(0,0)][usb_utils.INTERFACE_IN]

print(usb_utils.writeCommand(in_endpoint, '\x88'))
for i in range(1, 10):
  print(usb_utils.readData(dev_handler, dev_handler[0][(0,0)][0]))
  print(usb_utils.readData(dev_handler, dev_handler[0][(0,0)][1]))
  print(usb_utils.readData(dev_handler, dev_handler[0][(0,0)][3]))
  print("---------------------------")
print(usb_utils.writeCommand(in_endpoint, '\x89'))

# Detach device before exit from the script
# usb.util.dispose_resources(dev_handler)
