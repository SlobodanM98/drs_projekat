from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDesktopWidget, QLabel, QWidget, \
    QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys


class Projectile(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        slika = QPixmap("LaserT.png")
        self.setPixmap(slika.scaled(5, 30))
        self.resize(5, 30)




