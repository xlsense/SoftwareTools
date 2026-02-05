import cv2
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="IP Camera Zoom and Crop Example")
parser.add_argument("--ip", '-i', required=False, default='192.168.0.120', help="IP address of the camera (default: 192.168.0.120)")
parser.add_argument("--username", '-u', required=False, default='admin', help="Username login (default: admin)")
parser.add_argument("--password", '-pw', required=False, default='admin', help="Password login (default: admin)")
parser.add_argument("--port", '-p', required=False, type=int, default=554, help="RTSP port (default: 554)")
parser.add_argument("--stream_id", '-s', required=False, type=int, default=1, help="Stream ID used for the RTSP stream (default: 1)")
parser.add_argument("--max_zoom", type=int, required=False, default=10, help="Sets the maximum zoom factor (default: 10)")
parser.add_argument("--resolution_x", '-rx', type=int, required=False, default=1920, help="Width resolution (default: 1920)")
parser.add_argument("--resolution_y", '-ry', type=int, required=False, default=1080, help="Height resolution (default: 1080)")
args = parser.parse_args()


# Global variables
window_name = "ROI Frame"
zoom_factor = 1.1
mouse_x, mouse_y = -1, -1
zoom = 1
min_zoom = 1
max_zoom = args.max_zoom


# IP Camera RTSP URL parameters
ip = args.ip
username = args.username
password = args.password
port = args.port
stream_id = args.stream_id


# Callback for mouse events
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        global mouse_x, mouse_y
        mouse_x, mouse_y = x, y
    elif event == cv2.EVENT_MOUSEWHEEL:
        global crop_width, zoom, min_zoom, max_zoom
        if flags > 0:
            zoom *= zoom_factor
            zoom = min(zoom, max_zoom)
        elif flags < 0:
            zoom /= zoom_factor
            zoom = max(zoom, min_zoom)


def main():
    # Create a VideoCapture object and set mouse callback function
    rtsp_url = f"rtsp://{username}:{password}@{ip}:{port}/snl/live/1/{stream_id}"
    cap = cv2.VideoCapture(rtsp_url)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    # Set the frame width and height based on your camera's resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.resolution_x)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.resolution_y)

    # Create a window and set the mouse callback function
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_callback)

    
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Check if the frame was read successfully
        if not ret:
            print("Error: Could not read frame.")
            break

        # Calculate zoomed-in image size
        new_width = round(frame.shape[1] / zoom)
        new_height = round(frame.shape[0] / zoom)

        # Calculate offsets
        x = max(0, mouse_x)
        y = max(0, mouse_y)
        x_offset = round(x - x/zoom)
        y_offset = round(y - y/zoom)

        # Crop image
        roi = frame[
            y_offset: y_offset + new_height,
            x_offset: x_offset + new_width
        ]

        # Stretch image to full size
        roi = cv2.resize(roi, (frame.shape[1], frame.shape[0]))
        cv2.imshow(window_name, roi)
        
        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Keyboard interrupt detected")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()