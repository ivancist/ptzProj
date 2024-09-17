# Class Camera with methods to control the camera

# Zoom
# When receive a zoom value, set the zoom value to the camera
# http://192.168.0.90/axis-cgi/com/ptz.cgi?camera=1&zoom=8327&timestamp=1726212131092

# Position (center)
# When receive a pan value, set the pan value to the camera
# http://192.168.0.90/axis-cgi/com/ptz.cgi?camera=1&center=767,344&imagewidth=1280&imageheight=720

# Position (continuous move)
# When receive a continuous move value, set the continuous move value to the camera (needs to be stopped with 0,0)
# http://192.168.0.90/axis-cgi/com/ptz.cgi?camera=1&continuouspantiltmove=-23,0

import time
import requests
import cv2
from ultralytics import YOLO

class PTZ:
    def __init__(self, ip):
        self.ip = ip
        self.camera = 1
        self.resolution = 1080
        self.width = 1920
        self.height = 1080
        # self.videoCapture = cv2.VideoCapture('rtsp://'+self.ip+'/axis-media/media.amp')
        self.videoCapture = cv2.VideoCapture(0)

    def zoom(self, zoom):
        print("Zoom called")
        url = f'http://{self.ip}/axis-cgi/com/ptz.cgi?camera={self.camera}&zoom={zoom}&timestamp={int(time.time())}'
        # GET request to the camera
        r = requests.get(url)
        print("Zoom request sent")

    async def get_position(self):
        print("Get Position called")
        url = f'http://{self.ip}/axis-cgi/com/ptz.cgi?camera={self.camera}&query=position'
        # GET request to the camera
        r = requests.get(url)
        print("Get Position request sent")
        # Text response with 7 lines (key = value)
        # pan, tilt, zoom, focus, brightness, autofocus (on/off), autoiris (on/off)
        pan = r.text.split('\n')[0].split('=')[1]
        tilt = r.text.split('\n')[1].split('=')[1]
        # zoom = r.text.split('\n')[2].split('=')[1]
        return pan, tilt

    def center(self, x, y, width=None, height=None):
        print("Center called")
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        url = f'http://{self.ip}/axis-cgi/com/ptz.cgi?camera={self.camera}&center={x},{y}&imagewidth={width}&imageheight={height}'
        # GET request to the camera
        r = requests.get(url)
        print("Center request sent")

    def continuous_move(self, pan_speed, tilt_speed, object_detection=False):
        print("Continuous Move called")
        url = f'http://{self.ip}/axis-cgi/com/ptz.cgi?camera={self.camera}&continuouspantiltmove={pan_speed},{tilt_speed}'
        # GET request to the camera
        r = requests.get(url)
        print("Continuous Move request sent")

        if object_detection:
            obj = self.detect_object()
            if obj is not None:
                self.continuous_move(0, 0)

    def detect_object(self):
        print("Object Detection Started")
        model = YOLO('yolov10n.yaml')
        


    def wait_and_stop(self, time_to_wait):
        time.sleep(time_to_wait)
        self.continuous_move(0, 0)

    def move(self, pan, tilt):
        print("Move called")
        self.pan(pan)
        self.tilt(tilt)


    def pan(self, pan):
        print("Pan called")
        url = f'http://{self.ip}/axis-cgi/com/ptz.cgi?camera={self.camera}&pan={pan}'
        # GET request to the camera
        r = requests.get(url)
        print("Pan request sent")

    def tilt(self, tilt):
        print("Tilt called")
        url = f'http://{self.ip}/axis-cgi/com/ptz.cgi?camera={self.camera}&tilt={tilt}'
        # GET request to the camera
        r = requests.get(url)
        print("Tilt request sent")

    def get_resolution(self):
        return self.resolution, self.width, self.height

    def set_resolution(self, resolution):
        switch = {
            180: [320, 180],
            270: [480, 270],
            450: [800, 450],
            720: [1280, 720],
            1080: [1920, 1080]
        }

        if resolution not in switch:
            return

        self.resolution = resolution
        self.width = switch[resolution][0]
        self.height = switch[resolution][1]

    def set_preset(self, preset):
        print("Set Preset called")
        url = f'http://{self.ip}/axis-cgi/com/ptz.cgi?camera={self.camera}&setserverpresetname={preset}&timestamp={int(time.time())}'
        # GET request to the camera
        r = requests.get(url)
        print("Set Preset request sent")

    def remove_preset(self, preset):
        print("Remove Preset called")
        url = f'http://{self.ip}/axis-cgi/com/ptz.cgi?camera={self.camera}&removeserverpresetname={preset}&timestamp={int(time.time())}'
        # GET request to the camera
        r = requests.get(url)
        print("Remove Preset request sent")

    def goto_preset(self, preset):
        print("Goto Preset called")
        url = f'http://{self.ip}/axis-cgi/com/ptz.cgi?camera={self.camera}&gotoserverpresetname={preset}&timestamp={int(time.time())}'
        # GET request to the camera
        r = requests.get(url)
        print("Goto Preset request sent")

    def display(self):
        print("Display started")
        while True:
            ret, frame = self.videoCapture.read()
            if not ret:
                break
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        print("Display ended")