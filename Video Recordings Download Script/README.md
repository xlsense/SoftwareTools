# Camera Recordings Download Script
Basic python script to download the camera's onboard video recordings.

## Example
Command: python download_camera_recordings.py -s "2024-07-08 12:45:00" -e "2024-07-08 13:15:00" -bp "C:/test"
Result: The script will download all recordings which started after 2024-07-08 12:45:00 and before 2024-07-08 13:15:00, and save them to the "C:\test" directory.

## Usage
1. This script was tested with Python 32-bit version 3.11.4.
2. This script uses modules native to the standard 32-bit Python install. No external modules should need to be installed.
3. The lib folder must always be in the same directory as the python script.
4. Do not modify the internal subfolders and files within lib.
