#!/usr/bin/env python
#
# File: win_service_reboot.py
# Author: eXtoxesses
# Date: February 13, 2018
#
# (C) COPYRIGHT eXtoxesses 2018
# Released under the same license as Python 3.6.4
#
# If 'pywin32' package does not install win32service and win32api use 'pypiwin32'

from win32com.shell.shell import ShellExecuteEx
from win32com.shell import shellcon

import win32service
import win32serviceutil
import ctypes
import tools
# import win32con
import socket

def isAdmin() :
  if ctypes.windll.shell32.IsUserAnAdmin() :
    return True
  else :
    return False

  
def startStopService(service_name) :
  host_name = socket.gethostname();
  status = win32serviceutil.QueryServiceStatus(service_name, host_name)[1];
  
  try :
    if (status == win32service.SERVICE_RUNNING) :
      win32serviceutil.StopService(service_name, host_name);
      print("System stopped...");
    else :
      win32serviceutil.StartService(service_name, None, host_name);
      print("System started...");
      
  except RuntimeError as r_err:
    print("[LOG] " + r_err);


def toWinPathFormat(file_path) :
  out_path = ""
  for i in range(0, len(file_path)):
    if file_path[i] == '/':
      out_path += "\\"
    else:
      out_path += file_path[0][i]
  return out_path


def winSudo(cmd, parameters) :
  if type(parameters) is list :
    parameters = tools.list2String(parameters);
  proc_info = ShellExecuteEx(nShow = win32con.SW_SHOWNORMAL,
                            fMask = shellcon.SEE_MASK_NOCLOSEPROCESS,
                            lpVerb = 'runas',
                            lpFile = cmd,
                            lpParameters = parameters
                            )
  return proc_info;
