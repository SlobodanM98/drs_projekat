from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDesktopWidget, QWidget, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import sys


class Player(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        slika = QPixmap("rocket.png")
        self.setPixmap(slika.scaled(100, 100))
        self.resize(100, 100)

    def keyPressEvent(self, event):
        if(event.key() == Qt.Key_A and self.x() >= -10):
            self.move(self.x() - 5, self.y())
        elif(event.key() == Qt.Key_D and self.x() <= 610):
            self.move(self.x() + 5, self.y())

