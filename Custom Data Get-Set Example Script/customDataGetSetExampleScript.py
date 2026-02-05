import requests
import logging
import http.client as httplib
from urllib.error import HTTPError
from http import HTTPStatus
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="IP Camera Custom Data Get/Set Test Script using the Camera's API")
parser.add_argument("--ip", '-i', required=False, default='192.168.0.120', help="IP address of the camera (default: 192.168.0.120)")
parser.add_argument("--username", '-u', required=False, default='admin', help="Username login (default: admin)")
parser.add_argument("--password", '-pw', required=False, default='admin', help="Password login (default: admin)")
parser.add_argument("--port", '-p', required=False, default=80, help="HTTP port (default: 80)")
parser.add_argument("--action", '-a', type=str, required=True, default="get", help="API call action, choose between get or set (default: get)")
parser.add_argument("--data", '-d', type=str, required=False, default="", help="The data to save onto the camera, only used when action is 'set'")
args = parser.parse_args()

req_url = f'http://{args.ip}:{args.port}/cgi-bin/param.cgi?userName={args.username}&password={args.password}&action={args.action}&type=estdata'

# httplib.HTTPConnection.debuglevel = 1
# logging.basicConfig(level=logging.DEBUG)    # you need to initialize logging, 
#                                             # otherwise you will not see anything from requests
try:
    if args.action == "get":
      r = requests.get(req_url,timeout=10)
    elif args.action == "set":
      r = requests.get(req_url, data=args.data)
    
    if r.status_code == 200:
        print(f"Successfully sent: {req_url}")
        if args.action == 'set':
            print(f"Data sent: {args.data}")
        print(f"Received ({len(r.content)} bytes): {r.content}")
except requests.ConnectionError:
    print("Failed to connect")
    exit(1)  # Exit with error code 1
except HTTPError as e:
    print(f"HTTP Error: {e.code} {HTTPStatus(e.code).phrase}")
    exit(1)  # Exit with error code 1
except Exception as e:
    print(f"[ERROR]: {e}")
    exit(1)  # Exit with error code 1
