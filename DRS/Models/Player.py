import time
from threading import Thread

from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDesktopWidget, QWidget, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtGui
import sys


class Player(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        slika = QPixmap("rocket.png")
        self.setPixmap(slika.scaled(45 * self.parent().razmera_sirina, 70 * self.parent().razmera_visina))
        self.resize(80 * self.parent().razmera_sirina, 70 * self.parent().razmera_visina)
        self.keylist = []
        self.keys = []
        self.dozvola = True
        self.a_odpusteno = False
        self.d_odpusteno = False
        self.space_odpusteno = False


    def keyPressEvent(self, event):
        if(event.key() == Qt.Key_A):
            nit = Thread(target=self.pritisnutoA, args=[])
            nit.start()
        if (event.key() == Qt.Key_D):
            nit = Thread(target=self.pritisnutoD, args=[])
            nit.start()
        if event.key() == Qt.Key_Space and self.dozvola:
            nit = Thread(target=self.pritisnut_space, args=[])
            nit.start()


    def keyReleaseEvent(self, event):
        if (event.key() == Qt.Key_A):
            self.a_odpusteno = True
        if (event.key() == Qt.Key_D):
            self.d_odpusteno = True
        if (event.key() == Qt.Key_Space):
            self.space_odpusteno = True


    def pritisnut_space(self):
        if (self.parent().postoji_projectil == False):
            self.parent().projektil_kreiranje_signal.emit()


    def pritisnutoA(self):
        while self.a_odpusteno != True:
            self.parent().player_kretanje_signal.emit(1)
            time.sleep(0.05)

        self.a_odpusteno = False


    def pritisnutoD(self):
        while self.d_odpusteno != True:
            self.parent().player_kretanje_signal.emit(0)
            time.sleep(0.05)

        self.d_odpusteno = False