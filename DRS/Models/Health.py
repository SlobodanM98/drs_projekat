from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDesktopWidget, QLabel, QWidget, \
    QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys

class Zivot(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        slika = QPixmap('zivot.png')
        self.setPixmap(slika.scaled(30 * self.parent().razmera_sirina, 30 * self.parent().razmera_visina))
        self.resize(30 * self.parent().razmera_sirina, 30 * self.parent().razmera_visina)
        self.postoji = True