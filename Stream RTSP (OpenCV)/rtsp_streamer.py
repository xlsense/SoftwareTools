import cv2
import argparse

parser = argparse.ArgumentParser(description="Start RTSP stream on an ExcelSense IP Camera.")
parser.add_argument("--ip", type=str, required=True, default="192.168.0.120", help="IP address of the camera")
parser.add_argument("--uname", type=str, required=True, default="admin", help="Username login credential")
parser.add_argument("--pswd", type=str, required=True, default="admin", help="Password login credential")
parser.add_argument("--port", type=str, required=False, default="554", help="RTSP port of the camera")
parser.add_argument("--stream", type=str, required=True, default="1", help="Camera stream ID")
args = parser.parse_args()

rtsp_url = f'rtsp://{args.uname}:{args.pswd}@{args.ip}:{args.port}/snl/live/1/{args.stream}'
cap = cv2.VideoCapture(rtsp_url)
window_name = f'IP Camera RTSP Stream {args.stream}'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
initialized = False

print('Starting RTSP streaming program')

if not cap.isOpened():
    print("Error: Could not open RTSP stream.")
    exit()

while True:
    try:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read a frame from the RTSP stream.")
            break
        if initialized and cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            print('Stream window closed - exiting program')
            break
        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) == ord('q'):
            break
        initialized = True
    except KeyboardInterrupt:
        print('Keyboard interrupt - exiting program')
        break

cap.release()
cv2.destroyAllWindows()