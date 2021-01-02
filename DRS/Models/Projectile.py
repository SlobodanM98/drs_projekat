from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDesktopWidget, QLabel, QWidget, \
    QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys


class Projectile(QLabel):
    def __init__(self, parent=None, sirina = 3, duzina = 10, slikaa = "LaserT.png"):
        super().__init__(parent)
        slika = QPixmap(slikaa)
        self.setPixmap(slika.scaled(sirina * self.parent().razmera_sirina, duzina * self.parent().razmera_visina))
        self.resize(sirina * self.parent().razmera_sirina, duzina * self.parent().razmera_visina)




