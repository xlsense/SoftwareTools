from onvif import ONVIFCamera
import time

ip = '192.168.0.120'
uname = 'admin'
pswd = 'admin'
wsdl = r'c:\rd\repositories\python-onvif-zeep\wsdl'
shutter = 500
gain = 10
wdr = 'OFF'

if wdr == 'OFF':
    assert(shutter >= 50 and shutter <= 200000)
elif wdr == 'ON':
    assert(shutter >= 2000 and shutter <= 200000)
else:
    raise Exception('wdr must be either ON or OFF')

assert(gain >= 0 and gain <= 100)

onv_cam = ONVIFCamera(ip, 80, uname, pswd, wsdl)

media_service = onv_cam.create_media_service()
sources = media_service.GetVideoSources()
token = sources[0].token
im = onv_cam.create_imaging_service()

curr_settings = im.GetImagingSettings({'VideoSourceToken': token})
print(curr_settings)
# This will print a detailed list of available video options for reference:
# options = im.GetOptions({'VideoSourceToken': token})
# print(options)
print("Applying WDR setting...")
curr_settings['Exposure']['ExposureTime'] = 2000
curr_settings['WideDynamicRange']['Mode'] = wdr
im.SetImagingSettings({'VideoSourceToken': token, 'ImagingSettings': curr_settings})
time.sleep(1.0)
curr_settings = im.GetImagingSettings({'VideoSourceToken': token})

print("Applying shutter-speed and gain settings...")
curr_settings['Exposure']['Mode'] = "MANUAL" # AUTO is other option
curr_settings['Exposure']['Gain'] = gain
curr_settings['Exposure']['ExposureTime'] = shutter
im.SetImagingSettings({'VideoSourceToken': token, 'ImagingSettings': curr_settings})
time.sleep(1.0)

print("Validating settings...")
# Grab the actual settings
curr_settings = im.GetImagingSettings({'VideoSourceToken': token})
print("Gain: {0}".format(curr_settings['Exposure']['Gain']))
print("Shutter speed: {0}".format(curr_settings['Exposure']['ExposureTime']))
print('WDR Mode: {0}'.format(curr_settings['WideDynamicRange']['Mode']))