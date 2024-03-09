from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QToolBar, QStatusBar, QFileDialog, QComboBox, QVBoxLayout, QWidget
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap, QAction
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import os
import sys
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(QSize(600, 500))

        toolbar = QToolBar("My toolbar")
        toolbar.setIconSize(QSize(16,16))
        self.addToolBar(toolbar)

        self.camera = QCamera()
        self.viewfinder = QCameraViewfinder()
        self.camera.setViewfinder(self.viewfinder)
        self.camera.start()

#        self.available_cameras = QCameraInfo.availableCameras()

 #       if not self.available_cameras:
  #          sys.exit()

        self.select_camera(0)

        camera_selector = QComboBox()
        camera_selector.setStatusTip("Choose camera to take pictures")
        camera_selector.setToolTip("Select Camera")
        camera_selector.setToolTipDuration(2500)

        camera_selector.addItems([camera.description() for camera in self.available_cameras])
        camera_selector.currentIndexChanged.connect(self.select_camera)
        toolbar.addWidget(camera_selector)

        self.setWindowTitle("Image Editor")

        browse_action = QAction(QIcon("./Icons/blue-folder-horizontal-open"), "Browse image", self)
        browse_action.setStatusTip("Select image")
        browse_action.triggered.connect(self.browse_image)
        toolbar.addAction(browse_action)

        capture_action = QAction(QIcon("./Icons/camera.png"), "Click Photo", self)
        capture_action.setStatusTip("Capture Image")
        capture_action.triggered.connect(self.click_image)
        toolbar.addAction(capture_action)

        self.image_label = QLabel()
        self.setCentralWidget(self.viewfinder)

        self.status = QStatusBar(self)
        self.setStatusBar(self.status)

    def browse_image(self):
        # Open a file dialog to select an image
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select Image")
        # file_dialog.setFileMode(QFileDialog.AnyFile)  # QFileDialog.AnyFile and QFileDialog.Directory
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.bmp)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.image_path = selected_files[0]
                self.display_image()

    def display_image(self):
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size()))

    def select_camera(self, i):
        selected_camera = self.available_cameras[i]
        self.camera = QCamera(selected_camera)
        self.camera.setViewfinder(self.viewfinder)
        self.camera.start()

    def click_image(self):
        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
        capture = QCameraImageCapture(self.camera)

        def alert(msg):
            print("Error:", msg)

        capture.error.connect(alert)

        def image_captured(d, i):
            print("Image Captured:", str(self.save_seq))

        capture.imageCaptured.connect(image_captured)

        current_camera_name = self.available_cameras[0].description()
        self.save_seq = 0

        capture.capture(os.path.join(self.save_path, "%s-%04d-%s.jpg" % (current_camera_name, self.save_seq, timestamp)))
        self.save_seq += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

