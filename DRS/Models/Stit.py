from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDesktopWidget, QLabel, QWidget, \
    QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys

class Stit(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nivo_ostecenja = 0
        slika_stit = QPixmap("Stit.png")
        self.setPixmap(slika_stit.scaled(80 * self.parent().razmera_sirina, 60 * self.parent().razmera_visina))
        self.resize(80 * self.parent().razmera_sirina, 60 * self.parent().razmera_visina)