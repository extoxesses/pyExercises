#!/usr/bin/env python
#
# File: win_service_reboot.py
# Author: eXtoxesses
# Date: February 13, 2018
#
# (C) COPYRIGHT eXtoxesses 2018
# Released under the same license as Python 3.6.4

import winUAC

import socket
import sys
import os
import time
import win32service
import win32serviceutil

import fileUtils
# from distutils.command import win32_build_ext

if (len(sys.argv) < 4) :
  print("[ERROR] Runtime exception: invalid number of parameters!")

host_name = socket.gethostname()
service_name = sys.argv[1]

# If this script has not superuser, it relaunch itself with superuser permissions
if not winUAC.isAdmin() :
  print("[LOG] Script was running without superuser permissions!")
  procInfo = winUAC.winSudo("python.exe", sys.argv)
  print("[LOG] Call info: ", procInfo)

else :
  print("[LOG] Script was running with superuser permissions!")
  status = win32serviceutil.QueryServiceStatus(service_name, host_name)[1]

  # Check if the service is running ad stop it
  if (status == win32service.SERVICE_RUNNING) :
    win32serviceutil.StopService(service_name, host_name)
    print("Services" + service_name + " was stopped...")
  win32serviceutil.WaitForServiceStatus(service_name, win32service.SERVICE_RUNNING)
  
  # Copy all file of interests
  for file in sys.argv[3:]:
    src_path, file_name = os.path.split(file)
    fileUtils.copy(file, sys.argv[2] + "\\" + file_name, True)
  
  # Restart service
  win32serviceutil.StartService(service_name, None, host_name)
  print("Services" + service_name + " was restarted...")
