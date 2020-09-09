from PyQt5.QtWidgets import QApplication

from camera import Camera
from config import ROIConfiguration
from network import Yolo3
from view import StartWindow
import cv2

view_width = 1040

# Initiliaze configuration
print("Initialize ROI Configuration ...")
config = ROIConfiguration('config.ini')
config.initialize()

# Initiliaze camera
print("Initialize Camera ...")
source = config.video_source
if source == 'camera':
    source = 0
camera = Camera(source, view_width)
camera.initialize()

# Initialize network
print("Initialize Network ...")
net = Yolo3()
net.initialize("yolo3/")

# Start the application
print("Start Application ...")
app = QApplication([])
start_window = StartWindow(camera, net, config, view_width)
start_window.show()
app.exit(app.exec_())
