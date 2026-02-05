# File: trigger1700.py
# Description: Simple script to trigger the ToughEye-1700. Functionality is determined by the trigger sequence.
# ExcelSense Technologies Corp.
# Version 1.0.0
# Date Released: 2023.05.03

import logging
import requests
import io
import os
import time
import datetime
from datetime import datetime
import argparse
import sys
from urllib.error import HTTPError
from http import HTTPStatus

# arguments
parser = argparse.ArgumentParser(description="Trigger the ToughEye-1700.")
parser.add_argument("--ip", type=str, required=False, default="192.168.0.120", help="IP address of the camera")
parser.add_argument("--uname", type=str, required=False, default="admin", help="Username of the camera login")
parser.add_argument("--pswd", type=str, required=False, default="admin", help="Password of the camera login")
parser.add_argument("--repeat", type=str, required=False, default="1", help="Number of times to repeat the call")
parser.add_argument("--delay", type=str, required=False, default="10", help="Delay between consecutive calls (if numRepeat>1) in milliseconds")
args = parser.parse_args()

# HTTP request to trigger self-clean cycle on TE1700
req_url = "http://" + args.ip + "/cgi-bin/alarm.cgi?userName=" + args.uname + "&password=" + args.pswd + "&action=manualControl&alarmOutID=1&controlFlag=1"


# these two lines enable debugging at httplib level (requests->urllib3->httplib)
# you will see the REQUEST, including HEADERS and DATA, 
# and RESPONSE with HEADERS but without DATA.
# the only thing missing will be the response.body which is not logged.
try:
    import httplib
except ImportError:
    import http.client as httplib

httplib.HTTPConnection.debuglevel = 1
logging.basicConfig(level=logging.WARNING)  # you need to initialize logging, 
                                            # otherwise you will not see anything from requests

start_time = datetime.now()

for x in range(int(args.repeat)):
    try:
        print(f"Sending request #{x+1} at time: {(datetime.now()-start_time).total_seconds()*1000.0}ms")
        r = requests.get(req_url,timeout=10)
        if r.status_code == 200:
            print("Successful HTTP GET request sent.")
        if r.text.strip() == "OK":
            print("Success Clean Trigger command sent.")
        else:
            print(f"Clean Trigger command not accepted. Response from device: {r.text}")
        time.sleep(float(args.delay)/1000.0)
    except requests.ConnectionError:
        print("Failed to connect")
    except HTTPError as e:
        print(f"HTTP Error: {e.code} {HTTPStatus(e.code).phrase}")
    except Exception as e:
        print(f"[ERROR]: {e}")
