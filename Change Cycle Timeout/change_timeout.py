# File: change_timeout.py
# Description: Simple script to modify the delay between self-cleaning cycles
# ExcelSense Technologies Corp.
# Version 1.0.0
# Date Released: 2023.05.29

import logging
import requests
import io
import os
import time
import argparse
import sys

# arguments
parser = argparse.ArgumentParser(description="Change delay between self-cleaning cycles for ToughEye-1700")
parser.add_argument("--ip", type=str, required=False, default="192.168.0.120", help="IP address of the camera")
parser.add_argument("--uname", type=str, required=False, default="admin", help="Username of the camera login")
parser.add_argument("--pswd", type=str, required=False, default="admin", help="Password of the camera login")
parser.add_argument("--delay_minutes", type=int, required=False, default=1440, help="Delay between cleaning cycles, in minutes")
parser.add_argument('--enable', action='store_true')
parser.add_argument('--disable', dest='enable', action='store_false')
parser.set_defaults(enable=True)
args = parser.parse_args()

if args.delay_minutes < 1 or args.delay_minutes > 1440:
    print("Delay must be between 1-1440 minutes.")
    exit(-1)

url = "http://{0}/cgi-bin/param.cgi?userName={1}&password={2}&action=set&type=IOAlarm&ScheduledSelfClean=false&TimedSelfClean={3}&TimeOneHours=0&TimeOneMinutes=0&TimeTwoHours=0&TimeTwoMinutes=0&TimeThreeHours=0&TimeThreeMinutes=0&TimeInterval={4}".format(
    args.ip,
    args.uname,
    args.pswd,
    "true" if args.enable else "false",
    args.delay_minutes
)

print(url)

try:
    import httplib
except ImportError:
    import http.client as httplib

r = requests.get(url ,timeout=10)
if r.status_code == 200:
    print("Successfully modified delay between cleaning cycles")
    print(r.text)
else:
    print("Failed to modify delay between cleaning cycles. Status code: {0}".format(r.status_code))
