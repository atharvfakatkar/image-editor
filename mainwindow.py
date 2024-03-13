from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QToolBar, QStatusBar, QFileDialog, QComboBox, QVBoxLayout, QWidget, QGridLayout
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap, QAction
import os
import sys
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        toolbar = QToolBar("My toolbar")
        toolbar.setIconSize(QSize(16,16))
        self.addToolBar(toolbar)

        self.setWindowTitle("Image Editor")
        self.setGeometry(100,100,1080,720)

        browse_action = QAction(QIcon("./Icons/blue-folder-horizontal-open"), "Browse image", self)
        browse_action.setStatusTip("Select image")
        browse_action.triggered.connect(self.browse_image)
        toolbar.addAction(browse_action)

        capture_action = QAction(QIcon("./Icons/camera.png"), "Click Photo", self)
        capture_action.setStatusTip("Capture Image")
        capture_action.triggered.connect(self.click_image)
        toolbar.addAction(capture_action)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        self.image_label = QLabel()
        layout.addWidget(self.image_label)

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

