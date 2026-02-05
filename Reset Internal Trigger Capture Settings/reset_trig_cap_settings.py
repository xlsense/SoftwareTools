# File: reset_trig_cap_settings.py
# Description: Simple script to reset the internal trigger capture settings, required for correctly triggering a ToughEye-1700 to perform various functions such as self-cleaning.
# ExcelSense Technologies Corp.
# Version 1.0.0
# Date Released: 2025.09.23

import logging as l
from urllib.error import HTTPError
import requests
import http.client as httplib
from http import HTTPStatus
import argparse

DEFAULT_ALARM_OUT_CONFIGS = {
    "alarm_out_id":         1,
    "alarm_out_name":       'cleanTrigger',
    "alarm_mode":           2,
    "alarm_valid_signal":   1,
    "alarm_out_freq":       5,
    "alarm_time":           300
} 

def set_default_alarm_valid_signal(ip, uname, pswd) -> bool:
    set_url = f"http://{ip}/cgi-bin/param.cgi?userName={uname}&password={pswd}&action=set&type=alarmOut"
    set_url += f"&alarmOutID={DEFAULT_ALARM_OUT_CONFIGS['alarm_out_id']}&alarmOutName={DEFAULT_ALARM_OUT_CONFIGS['alarm_out_name']}"
    set_url += f"&alarmMode={DEFAULT_ALARM_OUT_CONFIGS['alarm_mode']}&alarmValidSignal={DEFAULT_ALARM_OUT_CONFIGS['alarm_valid_signal']}"
    set_url += f"&alarmOutFrequency={DEFAULT_ALARM_OUT_CONFIGS['alarm_out_freq']}&alarmTime={DEFAULT_ALARM_OUT_CONFIGS['alarm_time']}"
    
    set_resp = requests.request("GET", set_url)
    if set_resp.status_code != HTTPStatus.OK:
        l.error('Failed to set default Trigger Capture Settings, status code: {0}'.format(set_resp.status_code))
        return False
    return True

# arguments
parser = argparse.ArgumentParser(description="Reset internal trigger capture settings on the ToughEye-1700.")
parser.add_argument("--ip", type=str, required=False, default="192.168.0.120", help="IP address of the camera")
parser.add_argument("--uname", type=str, required=False, default="admin", help="Username of the camera login")
parser.add_argument("--pswd", type=str, required=False, default="admin", help="Password of the camera login")
args = parser.parse_args()

# set up HTTP logging
httplib.HTTPConnection.debuglevel = 1
l.basicConfig(level=l.INFO)

try:
    l.info(f"Sending API to reset trigger capture settings on camera at IP {args.ip}...")
    success = set_default_alarm_valid_signal(args.ip, args.uname, args.pswd)
    if success:
        l.info("Successfully reset trigger capture settings")
except requests.ConnectionError:
    l.error("Failed to connect")
except HTTPError as e:
    l.error(f"Status code: {e.code}. Detail: {HTTPStatus(e.code).phrase}")
except Exception as e:
    l.error(e)
