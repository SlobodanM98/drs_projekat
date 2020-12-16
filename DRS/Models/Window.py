import time
from threading import Thread

from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDesktopWidget, QLabel, QWidget, \
    QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap
import sys
from Models.Player import Player
from Models.Projectile import Projectile


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.player = Player(self)

        self.set_ui()

    def set_ui(self):
        self.setStyleSheet("background-color: black;")
        vbox = QVBoxLayout(self)

        self.player.projektil_signal.connect(self.kreiranje_projektila)

        self.setFixedSize(700, 800)
        vbox.addWidget(self.player)
        self.player.move(300, 700)
        self.player.setFocus()

        self.setLayout(vbox)
        self.setGeometry(600, 100, 500, 500)
        self.setWindowTitle("Space invader")
        self.show()

    @pyqtSlot()
    def kreiranje_projektila(self):
        projectile = Projectile(self)
        self.layout().addWidget(projectile)
        projectile.move(self.player.x()+47.5, self.player.y()-30)

