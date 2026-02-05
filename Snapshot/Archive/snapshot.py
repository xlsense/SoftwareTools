# Simple snapshot script for ToughEye-1700 and ToughCam-1000
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
parser = argparse.ArgumentParser(description="Retrieve snapshots from ToughCam-1000 or ToughEye-1700.")
parser.add_argument("--ip", type=str, required=True, help="IP address of the camera")
parser.add_argument("--uname", type=str, required=True, help="Username of the camera login")
parser.add_argument("--pswd", type=str, required=True, help="Password of the camera login")
parser.add_argument("--path", type=str, required=False, help="Path to save directory")
args = parser.parse_args()

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

quality = "9"   # mandatory, 1 (worst) ~ 9 (best)
url = "http://" + args.ip + "/cgi-bin/image.cgi?userName=" + args.uname + "&password=" + args.pswd + "&cameraID=1&quality=" + quality

try:
    r = requests.get(url,timeout=10)
    if args.path is not None:
        os.makedirs(args.path, exist_ok=True)
        fn = os.path.join(args.path, "snap_" + time.strftime("%Y%m%d_%H%M%S") + ".jpg")
    else:
        print("No path specified. Default to this directory")
        fn = "snap_" + time.strftime("%Y%m%d_%H%M%S") + ".jpg"
        
    file = open(fn, "wb")
    file.write(r.content)
    file.close()
except OSError:
    print("Could not open or write to file: " + fn)
    exit()
except KeyboardInterrupt:
    print("Keyboard interrupt, exiting")
    exit()
except requests.exceptions.RequestException as err:
    raise SystemExit(err)
except:
    exit()