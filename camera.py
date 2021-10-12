import cv2
from funcs import run

class VideoCapture(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)

    def __del__(self):
        self.cap.releast()
    
    def get_frame(self):
        flag = 0
        finalText = ""
        success, img = self.cap.read()

        img = run(img)

        success, jpeg = cv2.imencode(".jpg", img)
        return jpeg.tobytes()
