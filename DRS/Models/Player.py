import time
from threading import Thread

from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDesktopWidget, QWidget, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtGui
import sys


class Player(QLabel):

    game_over_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        slika = QPixmap("rocket.png")
        self.setPixmap(slika.scaled(45 * self.parent().razmera_sirina, 70 * self.parent().razmera_visina))
        self.resize(80 * self.parent().razmera_sirina, 70 * self.parent().razmera_visina)
        self.keylist = []
        self.keys = []
        self.a_odpusteno = False
        self.d_odpusteno = False
        self.game_over = False
        self.game_over_signal.connect(self.gasenje)

    def gasenje(self):
        self.game_over = True

    def keyPressEvent(self, event):
        if self.game_over is False:
            if (event.key() == Qt.Key_A):
                nit = Thread(target=self.pritisnutoA, args=[])
                nit.start()
            if (event.key() == Qt.Key_D):
                nit = Thread(target=self.pritisnutoD, args=[])
                nit.start()
            if event.key() == Qt.Key_Space:
                nit = Thread(target=self.pritisnut_space, args=[])
                nit.start()
        if (event.key() == Qt.Key_P and self.game_over):
            self.parent().nova_igra_signal.emit()
            self.game_over = False
            self.a_odpusteno = False
            self.d_odpusteno = False

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
        while self.a_odpusteno != True and self.game_over is False:
            self.parent().player_kretanje_signal.emit(1)
            time.sleep(0.05)

        self.a_odpusteno = False


    def pritisnutoD(self):
        while self.d_odpusteno != True and self.game_over is False:
            self.parent().player_kretanje_signal.emit(0)
            time.sleep(0.05)

        self.d_odpusteno = False