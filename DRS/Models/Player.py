import time
from threading import Thread

from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDesktopWidget, QWidget, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtGui
import sys


class Player(QLabel):

    projektil_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        slika = QPixmap("rocket.png")
        self.setPixmap(slika.scaled(100, 100))
        self.resize(100, 100)
        self.keylist = []
        self.keys = []
        self.dozvola = True
        self.a_odpusteno = False
        self.d_odpusteno = False

    '''def keyPressEvent(self, event):
        self.firstrelease = True
        astr = "pressed: " + str(event.key())
        print(astr)
        self.keylist.append(astr)
        self.keys.append(event.key())

    def keyReleaseEvent(self, event):
        print(event.key())
        if self.firstrelease == True:
            if event.key() == Qt.Key_A:
                self.a_odpusteno = True
            elif event.key() == Qt.Key_D:
                self.d_odpusteno = True
            self.processmultikeys(self.keylist, self.keys)

        self.firstrelease = False
        print(event.key())

        del self.keylist[-1]
        print(self.keylist)
        self.keys.remove(event.key())

    def processmultikeys(self, keyspressed, keys):
        print(keyspressed)
        for i in keys:
            if i == Qt.Key_A and self.x() >= -10:
                nit = Thread(target=self.pomeraj_a, args=[])
                nit.start()
            elif i == Qt.Key_D and self.x() <= 610:
                nit = Thread(target=self.pomeraj_d, args=[])
                nit.start()
            elif i == Qt.Key_G and self.dozvola:
                self.projektil_signal.emit()
                self.dozvola = False
                nit = Thread(target=self.space_blokada, args=[])
                nit.start()

    def space_blokada(self):
        time.sleep(0.5)
        self.dozvola = True

    def pomeraj_a(self):
        while (self.a_odpusteno == False):
            self.move(self.x() - 5, self.y())
            time.sleep(0.1)
            if self.x() < -10:
                break
        self.a_odpusteno = False
        if self.x() >= -10:
            self.move(self.x() - 5, self.y())

    def pomeraj_d(self):
        while (self.d_odpusteno == False):
            self.move(self.x() + 5, self.y())
            time.sleep(0.1)
            if self.x() > 610:
                break
        self.d_odpusteno = False
        if self.x() <= 610:
            self.move(self.x() + 5, self.y())'''


    def keyPressEvent(self, event):
        self.firstrelease = True
        print(event.text())
        self.keylist.append(event.key())

    def keyReleaseEvent(self, event):
        print("dd: {}".format(event.text()))
        if self.firstrelease == True:
            self.processmultikeys(self.keylist)

        self.firstrelease = False

        self.keylist.remove(event.key())

    def processmultikeys(self, keyspressed):
        for i in keyspressed:
            if i == Qt.Key_A and self.x() >= -10:
                self.move(self.x() - 5, self.y())
            elif i == Qt.Key_D and self.x() <= 610:
                self.move(self.x() + 5, self.y())
            elif i == Qt.Key_Space and self.dozvola:
                self.projektil_signal.emit()
                self.dozvola = False
                nit = Thread(target=self.space_blokada, args=[])
                nit.start()

    def space_blokada(self):
        time.sleep(0.5)
        self.dozvola = True