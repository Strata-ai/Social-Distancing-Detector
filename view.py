import numpy as np

from PyQt5.QtCore import Qt, QThread, QTimer
from PyQt5.QtGui import QPixmap, QFont, QImage, QCursor, QIntValidator
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QHBoxLayout, QApplication, QLabel, \
                            QDialog, QDialogButtonBox, QVBoxLayout, QLineEdit
from pyqtgraph import ImageView, PlotWidget, GraphicsView, ImageItem
import cv2


class PictureView(GraphicsView):
    def __init__(self, *args, **kwargs):
        super(PictureView, self).__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        print(event.pos())

    def mouseReleaseEvent(self, event):
        cursor = QCursor()
        print(cursor.pos())


class ConfigDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(ConfigDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Region of Interest Configuration")

        QBtn = QDialogButtonBox.Save | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        validator = QIntValidator(0, 1500)

        self.layout = QVBoxLayout()
        h_layout_1 = QHBoxLayout()
        h_layout_2 = QHBoxLayout()

        h_layout_1.addWidget(QLabel("Video Source:"))
        self.video_source = QLineEdit()
        h_layout_1.addWidget(self.video_source)

        v_layout_1 = QVBoxLayout()
        v_layout_1.addWidget(QLabel("Bottom Left - pixel (x, y):"))
        v_layout_1.addWidget(QLabel("Bottom Right - pixel (x, y):"))
        v_layout_1.addWidget(QLabel("Top Right - pixel (x, y):"))
        v_layout_1.addWidget(QLabel("Top Left - pixel (x, y):"))
        v_layout_1.addWidget(QLabel("Dimension - cm (width, depth):"))
        h_layout_2.addLayout(v_layout_1)

        v_layout_2 = QVBoxLayout()
        self.bl_x = QLineEdit()
        self.bl_x.setValidator(validator)
        v_layout_2.addWidget(self.bl_x)
        self.br_x = QLineEdit()
        self.br_x.setValidator(validator)
        v_layout_2.addWidget(self.br_x)
        self.tr_x = QLineEdit()
        self.tr_x.setValidator(validator)
        v_layout_2.addWidget(self.tr_x)
        self.tl_x = QLineEdit()
        self.tl_x.setValidator(validator)
        v_layout_2.addWidget(self.tl_x)
        self.width = QLineEdit()
        self.width.setValidator(validator)
        v_layout_2.addWidget(self.width)
        h_layout_2.addLayout(v_layout_2)

        v_layout_3 = QVBoxLayout()
        self.bl_y = QLineEdit()
        self.bl_y.setValidator(validator)
        v_layout_3.addWidget(self.bl_y)
        self.br_y = QLineEdit()
        self.br_y.setValidator(validator)
        v_layout_3.addWidget(self.br_y)
        self.tr_y = QLineEdit()
        self.tr_y.setValidator(validator)
        v_layout_3.addWidget(self.tr_y)
        self.tl_y = QLineEdit()
        self.tl_y.setValidator(validator)
        v_layout_3.addWidget(self.tl_y)
        self.depth = QLineEdit()
        self.depth.setValidator(validator)
        v_layout_3.addWidget(self.depth)
        h_layout_2.addLayout(v_layout_3)

        self.layout.addLayout(h_layout_1)
        self.layout.addLayout(h_layout_2)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class StartWindow(QMainWindow):
    def __init__(self, camera = None, net = None, config = None, image_width = 950):
        super().__init__()
        self.camera = camera
        self.net = net
        self.config = config
        self.image_width = image_width

        self.setFixedWidth(image_width + 78)
        self.setFixedHeight(780)
        
        self.central_widget = QWidget(self)

        self.label_logo = QLabel(self.central_widget)
        logo = QPixmap("logo.png")
        self.label_logo.setPixmap(logo)
        self.label_logo.setGeometry(20,20,181,81)
        self.label_logo.setScaledContents(True)
        
        self.label_logo_2 = QLabel(self.central_widget)
        logo_2 = QPixmap("logo_2.png")
        self.label_logo_2.setPixmap(logo_2)
        self.label_logo_2.setGeometry(670,30,206,61)
        self.label_logo_2.setScaledContents(True)

        self.button_config = QPushButton('Configuration', self.central_widget)
        self.button_config.setGeometry(240,30,191,61)
        font = QFont()
        font.setPointSize(24)
        self.button_config.setFont(font)
        self.button_config.clicked.connect(self.start_config)
        
        self.button_detection = QPushButton('Start Detection', self.central_widget)
        self.button_detection.setGeometry(450,30,191,61)
        font = QFont()
        font.setPointSize(24)
        self.button_detection.setFont(font)
        self.button_detection.clicked.connect(self.start_movie)

        #self.label_image = QLabel(self.central_widget)
        self.image_view = PictureView(self.central_widget)
        self.image_view.setGeometry(39,110,image_width,630)
        #self.image_view.hideAxis('left')
        #self.image_view.hideAxis('bottom')
        self.image_view.setStyleSheet("border :1px solid black;")
        #self.label_image.setGeometry(40,110,1067,600)
        #self.label_image.setScaledContents(True)
        #self.label_image.setStyleSheet("border :1px solid black;")

        self.setCentralWidget(self.central_widget)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_movie)

    def start_config(self):
        dlg = ConfigDialog(self)
        dlg.bl_x.setText(str(self.config.bl_x))
        dlg.bl_y.setText(str(self.config.bl_y))
        dlg.br_x.setText(str(self.config.br_x))
        dlg.br_y.setText(str(self.config.br_y))
        dlg.tl_x.setText(str(self.config.tl_x))
        dlg.tl_y.setText(str(self.config.tl_y))
        dlg.tr_x.setText(str(self.config.tr_x))
        dlg.tr_y.setText(str(self.config.tr_y))
        dlg.width.setText(str(self.config.width))
        dlg.depth.setText(str(self.config.depth))
        dlg.video_source.setText(self.config.video_source)

        if dlg.exec_():
            self.config.bl_x = int(dlg.bl_x.text())
            self.config.bl_y = int(dlg.bl_y.text())
            self.config.br_x = int(dlg.br_x.text())
            self.config.br_y = int(dlg.br_y.text())
            self.config.tl_x = int(dlg.tl_x.text())
            self.config.tl_y = int(dlg.tl_y.text())
            self.config.tr_x = int(dlg.tr_x.text())
            self.config.tr_y = int(dlg.tr_y.text())
            self.config.width = int(dlg.width.text())
            self.config.depth = int(dlg.depth.text())
            self.config.video_source = dlg.video_source.text()
            self.config.save()

    def update_image(self):
        frame = self.camera.get_frame()
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        #self.image_view.setImage(frame.T)
        image_item = ImageItem(frame)
        self.image_view.addItem(image_item)
        #height, width, channel = frame.shape
        #bytesPerLine = 3 * width
        #qimg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        #self.label_image.setPixmap(QPixmap(qimg))
        #self.update()
        #print(height, width)

    def update_movie(self):
        #print(self.camera.last_frame.shape)
        image_item = ImageItem(self.camera.last_frame)
        self.image_view.addItem(image_item)
        #self.image_view.setImage(self.camera.last_frame.T)

    def update_brightness(self, value):
        value /= 10
        self.camera.set_brightness(value)

    def start_movie(self):
        self.movie_thread = MovieThread(self.camera, self.net, self.config)
        self.movie_thread.start()
        self.update_timer.start(30)


class MovieThread(QThread):
    def __init__(self, camera, net, config):
        super().__init__()
        self.camera = camera
        self.net = net
        self.config = config

    def run(self):
        #self.camera.acquire_movie(500)
        self.camera.detect_in_movie(500, self.net, self.config)

if __name__ == '__main__':
    app = QApplication([])
    window = StartWindow()
    window.show()
    app.exit(app.exec_())
