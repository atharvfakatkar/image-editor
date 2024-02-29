from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QToolBar, QStatusBar, QFileDialog
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon, QPixmap
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(QSize(600, 500))

        toolbar = QToolBar("My toolbar")
        toolbar.setIconSize(QSize(16,16))
        self.addToolBar(toolbar)

        self.setWindowTitle("Image Editor")
        
        button_action = QAction(QIcon("./Icons/blue-folder-horizontal-open"), "Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.browse_image)
        toolbar.addAction(button_action)

        self.image_label = QLabel()
        self.setCentralWidget(self.image_label)
        
        self.setStatusBar(QStatusBar(self))

    def browse_image(self):
        # Open a file dialog to select an image
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select Image")
        #file_dialog.setFileMode(QFileDialog.AnyFile)       #QFileDialog.AnyFile and QFileDialog.Directory
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.bmp)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.image_path = selected_files[0]
                self.display_image()

    def display_image(self):
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size()))

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
