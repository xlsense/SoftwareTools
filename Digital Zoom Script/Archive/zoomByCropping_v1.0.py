import cv2

crop_width, crop_height = 500, 300  # "Zoomed-in" (i.e. cropped view) window dimensions
original_window_name = "Original Frame"
zoomed_in_window_name = "Zoomed-In ROI"
mouse_x, mouse_y = -1, -1

# IP Camera RTSP URL parameters
ip = "192.168.0.120"
username = "admin"
password = "admin"
port = 554
stream_id = 1  # main (base) stream is stream ID #1

# Callback function for mouse events
def mouse_callback(event, x, y, flags, param):
    global mouse_x, mouse_y

    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x, mouse_y = x, y

# IP camera URL
ipc_rtsp_url = f"rtsp://{username}:{password}@{ip}:{port}/snl/live/1/{stream_id}"

# Camera stream resolution
resX = 1920
resY = 1080

# Create a VideoCapture object and set mouse callback function
cap = cv2.VideoCapture(ipc_rtsp_url)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Set the frame width and height based on your camera's resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, resX)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resY)

# Create a window and set the mouse callback function
cv2.namedWindow(original_window_name)
cv2.namedWindow(zoomed_in_window_name)
cv2.setMouseCallback(original_window_name, mouse_callback)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Check if the frame was read successfully
    if not ret:
        print("Error: Could not read frame.")
        break
    
    # Calculate the coordinates for the region of interest (ROI) based on the mouse pointer
    x = max(0, mouse_x - crop_width // 2)
    y = max(0, mouse_y - crop_height // 2)

    # Crop the frame to the specified ROI
    roi = frame[y:y + crop_height, x:x + crop_width]

    # Display the original frame and the zoomed-in ROI
    cv2.imshow(original_window_name, frame)
    cv2.imshow(zoomed_in_window_name, roi)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()