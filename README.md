# Top-level Directory for Scripts & Tools

ExcelSense Technologies Corp.  
Last Updated On: 2024.07.12  

## Description
This directory holds a number of scripts and software tools that can be used with ExcelSense products, namely the camera module within ToughEye-1700 and ToughCam-1000.

## Disclaimer
The software scripts and tools available in this directory are provided "as is" without any warranties or guarantees of any kind.
They are intended as examples and may need to be modified to meet the specific requirements of your application.

## List of Available Scripts
1. Change Cycle Timeout: Simple python script to modify the delay between self-cleaning cycles.
2. Custom Data Get/Set Example: Basic implementation of the get/set functionality of the custom data string feature, which is available only on Gen2 FW v3.6.1607.1006.272.0.7.4.18 or later.
3. Digital Zoom Script: Python script which streams the live view of the camera through RTSP and zooms into a region of interest using the mouse wheel.
4. Intrinsic Calibration Uploader: App for uploading the intrinsic camera sensor calibration from 
a .txt file to the camera. This repository contains the apps documentation and sample data only. The .exe is available here: https://storage.googleapis.com/public-assets.excelsensetechnologies.com/software/camera-intrinsic-calibration-uploader/camera-sensor-intrinsic-calibration-uploader-1.0.0.exe
5. Latency Analysis using Timestamps from Gstreamer: Python script which uses the Gstreamer library to read camera-based per-frame timestamps.
6. Live Video Recorder: Python script used to record the live RTSP stream, and save it to a file on disc.
7. Reading Image Settings using ONVIF: Python script which reads camera image sensor settings through ONVIF, using the python-onvif-zeep library.
8. Snapshot: Python script which takes a single snapshot from the camera module.
9. Stream RTSP (OpenCV): Python script to stream live video through RTSP using the OpenCV library.
10. Trigger Command Script - Single Cycle: Script to send a single trigger to the camera; available in Python, C#, and batch file implementations.
11. Trigger Sequence Script: Python script used to send consecutive triggers to the TE-1700. Can be used to control the LEDs on the TE-1700 with Integrated Visible Light.
12. Video Recordings Download Script: Python script used to download recordings from the camera module. Only compatible with cameras with loaded onboard storage option.
13. Video Recordings Download Tool (GUI): Light-weight GUI application used to download recordings from the camera module. Only compatible with cameras with loaded onboard storage option.
14. Web Trigger UI: Light-weight GUI application used to send on-demand trigger commands to multiple cameras.