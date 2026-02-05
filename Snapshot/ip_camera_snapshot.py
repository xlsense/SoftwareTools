import cv2
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description="Snapshot script for TE-1700 and TC-1000.")
parser.add_argument("--ip_address", '-ip', required=False, type=str, default="192.168.0.120", help="IP address of the camera (default: 192.168.0.120)")
parser.add_argument("--username", '-uname', required=False, type=str, default="admin", help="Username of the camera (default: admin)")
parser.add_argument("--password", '-pswd', required=False, type=str, default="admin", help="Password of the camera (default: admin)")
parser.add_argument("--rtsp_port", '-rp', required=False, type=int, default=554, help="RTSP port (default: 554)")
parser.add_argument("--stream_id", '-sid', required=False, type=int, default=1, help="Stream ID to capture images from (default: 1)")
parser.add_argument("--show", '-s', action="store_true", help="Display the captured frame")
args = parser.parse_args()

rtsp_stream_url = f"rtsp://{args.username}:{args.password}@{args.ip_address}:{args.rtsp_port}/snl/live/1/{args.stream_id}"
capture = cv2.VideoCapture(rtsp_stream_url)

if (capture.isOpened()):
    (status_capture, frame) = capture.read()
    if (status_capture):
        fn = 'snap_' + datetime.now().strftime("%Y%m%d-%H%M%S") + '.png'
        print(f"Saving captured image to: '{fn}'")
        cv2.imwrite(filename=fn, img=frame)
        if args.show:
            cv2.imshow('Frame', frame)
            cv2.waitKey(0)  # Wait indefinitely for a key press
            cv2.destroyAllWindows()  # Close all OpenCV windows
    else:
        print("Failed to capture image")