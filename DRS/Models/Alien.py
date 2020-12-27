from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDesktopWidget, QLabel, QWidget, \
    QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys

class Alien(QLabel):
    def __init__(self, stringSlika, red, kolona, parent=None):
        super().__init__(parent)
        slika = QPixmap(stringSlika)
        self.setPixmap(slika.scaled(30, 20))
        self.resize(30, 20)
        self.postoji = True
        self.red = red
        self.kolona = kolona


