#!/usr/bin/env python
#
# File: usb_interface.py
# Author: eXtoxesses
# Date: March, 2018
#
# (C) COPYRIGHT eXtoxesses 2018
# Released under the same license as Python 3.6.4

import usb.backend.libusb1
import usb.core
import usb.util
import sys


## Tablet commands
VENDOR_ID = 0x04D8
DEVICE_ID = 0xF0B1
INTERFACE_IN = 2

TOGLE_LED = '\x40'
LED_ON = '\x41'
LED_OFF = '\x42'

BACKLIGHT_ON = '\x25'
BACKLIGHT_OFF = '\x29'
BACKLIGHT_UP = '\x23'
BACKLIGHT_DOWN = '\x24'
BACKLIGHT_SWITCH_STATUS = '\xC2' # Not clear what this command does

RESET = '\x22'
DETACH_DEVICE = '\x10'
GET_STATUS = '\x26'
SET_STATUS = '\x27'

GET_FW_VERSION = '\x01'
GET_TIME = '\x03'

# DIGITIZER
DIGITIZER_RESET = '\x52'
ENABLE_DIGITIZER = '\x86'
DISABLE_DIGITIZER = '\x87'
DIGITIZER_STATUS = '\xC0'
ENABLE_ENCRIPTION = '\x56'
DISABLE_ENCRIPTION = '\x57'
ENCRIPTION_STATUS = '\xC3'
ENABLE_BUFFERING = '\xA1'
DISABLE_BUFFERING = '\xA2'

# TOUCH


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
          except usb.core.USBError as err:
            msg = "Could not detach kernel driver from interface(" + interface.bInterfaceNumber + "): " + str(err)
            sys.exit(msg)
  
  except NotImplementedError as err:
    print("[ERROR] Impossible to find 'detach_kernel_driver' function. Device handler is returned without detach it!\n")
  
  device.set_configuration()
  return device


def readData(dev_handler, endpoint):
  try:
    data = dev_handler.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
    return data
  except usb.core.USBError as e:
    print("[ERROR] Impossibile read data from given endpoint")


def writeCommand(endpoint, command):
  return endpoint.write(command)
