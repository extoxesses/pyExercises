#!/usr/bin/env python
#
# File: win_service_reboot.py
# Author: eXtoxesses
# Date: February 13, 2018
#
# (C) COPYRIGHT eXtoxesses 2018
# Released under the same license as Python 3.6.4

import winUAC

import shutil
import socket
import sys
import time
import os
import win32service
import win32serviceutil

import fileinput
import fileUtils

if (len(sys.argv) < 4) :
  print("[ERROR] Runtime exception: invalid number of parameters!");

host_name = socket.gethostname();
service_name = sys.argv[1];

# If this script has not superuser, it relaunch itself with superuser permissions
if not winUAC.isAdmin() :
  print("[LOG] Script was running without superuser permissions!")
  procInfo = winUAC.winSudo("python.exe", sys.argv)
  print("[LOG] Call info: ", procInfo)

else :
  print("[LOG] Script was running with superuser permissions!");
  status = win32serviceutil.QueryServiceStatus(service_name, host_name)[1];

  if (status == win32service.SERVICE_RUNNING) :
    win32serviceutil.StopService(service_name, host_name);
    print("Services" + service_name + " was stopped...");

  copyFileList(getFileList(sys.argv), sys.argv[2]);

  win32serviceutil.StartService(service_name, None, host_name);
  print("Services" + service_name + " was restarted...");


def copyFileList(list, dst_root) :
  for file in list :
    src_path, file_name = os.path.split(file);
    fileUtils.copy(file, dst_root + file_name, True);
    
def getFileList(params) :
  l = len(params);
  input_files = list();
  for i in range(3, l) :
    input_files[i - 3] = params[i];
  return input_files;
  