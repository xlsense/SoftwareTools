# File: cycle.py
# Description: Simple script to trigger a self-cleaning cycle on the ToughEye-1700
# ExcelSense Technologies Corp.
# Version 1.0.0
# Date Released: 2021.12.09

import logging
import requests
import io
import os
import time
import argparse
import sys

# arguments
parser = argparse.ArgumentParser(description="Trigger self-cleaning cycle on the ToughEye-1700.")
parser.add_argument("--ip", type=str, required=False, default="192.168.0.120", help="IP address of the camera")
parser.add_argument("--uname", type=str, required=False, default="admin", help="Username of the camera login")
parser.add_argument("--pswd", type=str, required=False, default="admin", help="Password of the camera login")
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
logging.basicConfig(level=logging.DEBUG)    # you need to initialize logging, 
                                            # otherwise you will not see anything from requests
try:
    r = requests.get(req_url,timeout=10)
    if r.status_code == 200:
        print("Successfully sent clean trigger command through HTTP")
except requests.ConnectionError:
    print("Failed to connect")
except HTTPError as e:
    print(f"HTTP Error: {e.code} {HTTPStatus(e.code).phrase}")
except Exception as e:
    print(f"[ERROR]: {e}")
