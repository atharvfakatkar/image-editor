from PyQt6.QtWidgets import *
from PyQt6.QtMultimediaWidgets import *
from PyQt6.QtMultimedia import *
import os
import sys
import time


class Camera(QMainWindow):
    def __init__(self):
        super().__init__()
        

        self.available_camera = QCameraInfo.available_camera()

        if not self.available_camera:
            sys.exit()

        self.viewfinder = QCameraViewfinder()
        self.viewfinder.show()

        self.select_camera(0)



