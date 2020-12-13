from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDesktopWidget, QLabel, QWidget, \
    QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import Images
import sys
from Models.Player import Player


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.set_ui()

    def set_ui(self):
        self.setStyleSheet("background-color: black;")
        vbox = QVBoxLayout(self)

        self.player = Player(self)
        self.setFixedSize(700, 800)
        vbox.addWidget(self.player)
        self.player.move(300, 700)
        self.player.setFocus()

        self.setLayout(vbox)
        self.setGeometry(600, 100, 500, 500)
        self.setWindowTitle("Space invader")
        self.show()

