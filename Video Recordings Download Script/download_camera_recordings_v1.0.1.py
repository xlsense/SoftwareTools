"""
    Author: ExcelSense Technologies Corp.
    Name: download_camera_recordings.py
    Version: 1.0.1
    Description: Basic implementation of downloading camera recordings from the ExcelSense IP cameras. 
                 The script uses a 32-bit version of Python, and accepts in-line command arguments (use --h or see README file for details).
                 Press Ctrl-C anytime, including during a download, to exit the program.
    Version History:
        1.0.0: Initial release
        1.0.1: Minor improvements (e.g. show_rec and skip_downloads flags)
"""

import json
import os, os.path
from datetime import datetime
import logging as l
import argparse
from lib.camera_library import *

parser = argparse.ArgumentParser(description="Download tool for local onboard video recordings.")
parser.add_argument("--ip", required=False, default='192.168.0.120', help="IP address of the camera (default: 192.168.0.120).")
parser.add_argument("--username", required=False, default='admin', help="Username login (default: admin).")
parser.add_argument("--password", required=False, default='admin', help="Password login (default: admin).")
parser.add_argument("--port", required=False, type=int, default=30001, help="Control port (default: 30001).")
parser.add_argument("--start_date", required=True, type=str, help='Start date to search for recordings, in the format: "2024-07-09 00:00:00" (including the quotations).')
parser.add_argument("--end_date", required=True, type=str, help='End date to search for recordings, in the format: "2024-07-09 00:00:00" (including the quotations).')
parser.add_argument("--path", required=False, type=str, default=".", help="Path where recordings are to be saved.")
parser.add_argument("--show_rec", action="store_true", help="Print all recordings in the date range.")
parser.add_argument("--skip_download", action="store_true", help="Skip the download process. If --show_rec flag is given, the script will only show recordings without downloading.")
args = parser.parse_args()

l.basicConfig(
    level=l.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        l.FileHandler("info.log"),
        l.StreamHandler()
    ]
)

def cam_init():
    l.info("Initializing camera...")
    sdk.sdks_dev_init()

def cam_connect(ip_address, control_port, username, password):
    l.info("Connecting to camera...")
    global handle
    handle = sdk.sdks_dev_conn(ip_address, control_port, username, password)
    if handle == -508 or handle == -507:
        l.error('Could not connect. Invalid username or password, please try again')
    elif handle == 0:
        l.error('Could not connect. Timeout during connection. Please check IP address')
    elif handle < 0:
        l.error(f'Could not connect. Unknown error, Error code: {handle}')
    return handle

def cam_disconnect():
    l.info("Disconnecting from camera...")
    sdk.sdks_dev_conn_close(handle)

def get_date_list(start_date, end_date):
    l.info("Searching for list of all available dates...")
    date_list = sdk.sdks_dev_pb_date_list(handle, 1, 1, start_date.split(' ')[0], end_date.split(' ')[0])
    return date_list

def get_recordings_list(date_list, print_list=True):
    l.info("Searching for list of all available recordings...")
    if date_list is None:
        return None
    
    global handle
    all_recordings = {"data": []}
    for rd in json.loads(date_list)["data"]:
        rec_list_str = sdk.sdks_dev_pb_get_rec_list(handle, 1, 1, rd + " 00:00:00", rd + " 23:59:59")
        rec_list = json.loads(rec_list_str)
        all_recordings["data"].extend(rec_list["data"])
    
    if print_list:
        print(json.dumps(all_recordings, indent=4))
    return json.dumps(all_recordings)

def start_backup(start_date, end_date, rec_list, path):
    if rec_list is None:
        l.warning("No recordings found. Exiting script")
        return
    
    l.info("Starting download process...")
    global current_record, handle # want to modify global variables here, so need the global keyword
    rec_count = 0
    for rec in json.loads(rec_list)["data"]:
        try:
            backup_path = os.path.join(path, rec['s_time'].split(' ')[0])
            os.makedirs(backup_path, exist_ok=True)
        except FileNotFoundError:
            l.error("Unable to create directory. Cancelling download")
            return
        
        sf = "%Y-%m-%d %H:%M:%S"
        stime = datetime.strptime(rec["s_time"], sf)
        etime = datetime.strptime(rec["e_time"], sf)
        user_stime = datetime.strptime(start_date, sf)
        user_etime = datetime.strptime(end_date, sf)
        
        # download recording only if the user-input start time is between its start and end times
        if user_stime >= stime and user_stime < etime:
            rec_count += 1
            rec_log = f"Starting download #{rec_count}, from {start_date} to {end_date}"
            l.info(rec_log)

            filename_prefix = f"REC_{start_date.replace('-','').replace(' ','-').replace(':','')}_to_{end_date.replace('-','').replace(' ','-').replace(':','')}"
            current_record = sdk.sdks_md_rec_download_start(handle, 1, 1, start_date, end_date, backup_path, filename_prefix)
            pct_completion = sdk.sdks_md_rec_percent(handle, current_record)
            while pct_completion < 100:
                if pct_completion % 1 == 0:
                    print(f"\rDownloading... {pct_completion}%", end="", flush=True)
                pct_completion = sdk.sdks_md_rec_percent(handle, current_record)
            print(f"\rDownloading file: 'REC_{rec['s_time']}'... {pct_completion}%", flush=True)
            l.info(f"File #{rec_count} download complete")

            if len(json.loads(rec_list)["data"]) > 1:
                l.info("Disconnecting and reconnecting to camera to get the next recording")
                cam_disconnect()
                cam_connect(args.ip, args.port, args.username, args.password)

def stop_backup():
    l.info("Stopping download process")
    global current_record
    if current_record > 0: # still recording, so stop recording
        sdk.sdks_md_rec_download_stop(handle, current_record)
        current_record = 0


if __name__ == "__main__":    
    current_record = False
    handle = 0
    dll_path = os.path.join(os.getcwd(), r'lib\sdk\x86\sdk.dll')
    sdk = CameraLibrary(dll_path)
    try:
        l.info("Starting program")
        cam_init()
        handle = cam_connect(args.ip, args.port, args.username, args.password)
        date_list = get_date_list(args.start_date, args.end_date)
        rec_list = get_recordings_list(date_list, print_list=args.show_rec)
        if not args.skip_download:
            start_backup(args.start_date, args.end_date, rec_list, args.path)
    except KeyboardInterrupt:
        l.info("Detected keyboard interrupt")
        stop_backup()
    except Exception as e:
        l.error(e)
    finally:
        l.info("Exiting program")
        sdk.sdks_dev_quit()
