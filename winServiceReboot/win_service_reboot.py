#!/usr/bin/env python
#
# File: win_service_reboot.py
# Author: eXtoxesses
# Date: February 13, 2018
#
# (C) COPYRIGHT eXtoxesses 2018
# Released under the same license as Python 3.6.4

import winUAC
import sys
import time
import win32serviceutil

if not winUAC.isAdmin() :
  print("[LOG] Script was running without superuser permissions!")
  procInfo = winUAC.winSudo("python.exe", sys.argv)
  print("[LOG] Call info: ", procInfo)
else :
  service_name = sys.argv[1]
  service = win32serviceutil.LocateSpecificServiceExe(service_name)
  print(service)
  # win32serviceutil.StopService(service)
  win32serviceutil.StartService(service)

time.sleep(5)