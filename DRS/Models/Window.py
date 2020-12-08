from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
                             QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtCore import Qt
import sys


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.set_ui()

    def set_ui(self):
        self.setGeometry(300, 300, 550, 250)
        self.setWindowTitle('Space Invaders')
        self.show()
