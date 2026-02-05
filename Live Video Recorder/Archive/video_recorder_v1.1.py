import os
import subprocess
import argparse

parser = argparse.ArgumentParser(description="Records files from RTSP stream", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--ip', '-i', type=str, default="192.168.0.120", help="IP Address of the camera")					
parser.add_argument('--username', '-u', type=str, default='admin', help="Username to access the camera")	
parser.add_argument('--password', '-pw', type=str, default='admin',help="Password to access the camera")
parser.add_argument('--port', '-pt', type=int, default=554, help="RTSP port of the camera")
parser.add_argument('--output_path', type=str, help="Directory where video files are saved")
parser.add_argument('--ffmpeg_path', type=str, help="Full path to the ffmpeg.exe file")
parser.add_argument('--segtime', '-s', type=int, default=300, help='Duration of each video segment, in seconds')
args = parser.parse_args()

stream_url = "rtsp://{0}:{1}@{2}:{3}/snl/live/1/1".format(args.username, args.password, args.ip, args.port)

if not os.path.exists(args.output_path):
    os.mkdir(args.output_path)

output_format = os.path.join(args.output_path, '%Y-%m-%d_%H.%M.%S.mp4')

command_line = "{0} -stimeout 5000000 -i {1} -an -vcodec copy -segment_time {2} -f segment -strftime 1 -hide_banner -loglevel quiet -stats {3}".format(args.ffmpeg_path, stream_url, args.segtime, output_format)
print(command_line)
print("Launching ffmpeg recorder")
while True:    
    try:
        result = subprocess.run(command_line)

        if result.returncode == 0:
            print('FFMPEG lost RTSP connection')
        elif result.returncode == 1:
            print('Connection timed out, retrying...')
        else:
            print('Unknown return code: {0}'.format(result.returncode))
    except KeyboardInterrupt:
        print('Keyboard interrupt detected... exiting.')
        exit(0)

