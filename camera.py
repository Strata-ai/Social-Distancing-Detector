import numpy as np
import cv2


class Camera:
    def __init__(self, cam_num, view_width = None):
        self.cam_num = cam_num
        self.view_width = view_width
        self.cap = None
        self.last_frame = np.zeros((1,1))

    def initialize(self):
        self.cap = cv2.VideoCapture(self.cam_num)

    def resize_frame(self, frame, width):
        (h, w) = frame.shape[:2]
        h = int(width * h * 1.0 / w )
        return cv2.resize(frame, (width, h), interpolation = cv2.INTER_AREA)

    def get_frame(self):
        ret, frame = self.cap.read()
        if self.view_width:
            frame = self.resize_frame(frame, self.view_width)
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def acquire_movie(self, num_frames):
        movie = []
        for _ in range(num_frames):
            self.last_frame = self.get_frame()
            movie.append(self.last_frame)
        return movie

    def detect_in_movie(self, num_frames, net, config):
        for _ in range(num_frames):
            frame = net.detect_people(self.get_frame(), config)
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.last_frame = cv2.flip(frame, 0)


    def set_brightness(self, value):
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, value)

    def get_brightness(self):
        return self.cap.get(cv2.CAP_PROP_BRIGHTNESS)

    def close_camera(self):
        self.cap.release()

    def __str__(self):
        return 'OpenCV Camera {}'.format(self.cam_num)


if __name__ == '__main__':
    cam = Camera(0)
    cam.initialize()
    print(cam)
    frame = cam.get_frame()
    print(frame)
    cam.set_brightness(1)
    print(cam.get_brightness())
    cam.set_brightness(0.5)
    print(cam.get_brightness())
    cam.close_camera()
