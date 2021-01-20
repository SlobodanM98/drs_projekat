import time
from threading import Thread

from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDesktopWidget, QWidget, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtGui
import sys


class Player(QLabel):

    game_over_signal = pyqtSignal()
    game_on_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        slika = QPixmap("rocket.png")
        self.setPixmap(slika.scaled(45 * self.parent().razmera_sirina, 70 * self.parent().razmera_visina))
        self.resize(80 * self.parent().razmera_sirina, 70 * self.parent().razmera_visina)
        self.keylist = []
        self.keys = []
        self.a_odpusteno = False
        self.d_odpusteno = False
        self.na_strelice = False
        self.na_ad = False
        self.game_over = False
        self.izabrano_kretanje = False
        self.game_over_signal.connect(self.gasenje)
        self.game_on_signal.connect(self.paljenje)

    def gasenje(self):
        self.game_over = True

    def paljenje(self):
        self.game_over = False
        self.izabrano_kretanje = False
        self.a_odpusteno = False
        self.d_odpusteno = False
        self.na_strelice = False

    def keyPressEvent(self, event):
        if self.izabrano_kretanje:
            if self.game_over is False:
                if self.na_ad:
                    if event.key() == Qt.Key_A:
                        nit = Thread(target=self.pritisnutoA, args=[])
                        nit.start()
                    if event.key() == Qt.Key_D:
                        nit = Thread(target=self.pritisnutoD, args=[])
                        nit.start()
                elif self.na_strelice:
                    if event.key() == Qt.Key_Right:
                        nit2 = Thread(target=self.pritisnutoD, args=[])
                        nit2.start()
                    if event.key() == Qt.Key_Left:
                        nit2 = Thread(target=self.pritisnutoA, args=[])
                        nit2.start()
                if event.key() == Qt.Key_Space:
                    nit = Thread(target=self.pritisnut_space, args=[])
                    nit.start()
        else:
            if event.key() == Qt.Key_S:
                self.na_strelice = True
                self.izabrano_kretanje = True
                self.parent().pokreni_vanzemaljce_signal.emit()
                self.parent().labela_izbor_igranja.setHidden(True)
            if event.key() == Qt.Key_G:
                self.na_ad = True
                self.izabrano_kretanje = True
                self.parent().pokreni_vanzemaljce_signal.emit()
                self.parent().labela_izbor_igranja.setHidden(True)
        #if event.key() == Qt.Key_P and self.game_over:
            #self.parent().nova_igra_signal.emit(0)
            #self.game_over = False
            #self.a_odpusteno = False
            #self.d_odpusteno = False
            #self.na_strelice = False
            #self.na_ad = False
            #self.parent().labela_izbor_igranja.setHidden(False)
            #self.izabrano_kretanje = False


    def keyReleaseEvent(self, event):
        if self.na_ad:
            if event.key() == Qt.Key_A:
                self.a_odpusteno = True
            if event.key() == Qt.Key_D:
                self.d_odpusteno = True
        elif self.na_strelice:
            if event.key() == Qt.Key_Right:
                self.d_odpusteno = True
            if event.key() == Qt.Key_Left:
                self.a_odpusteno = True
        if event.key() == Qt.Key_Space:
            self.space_odpusteno = True




    def pritisnut_space(self):
        if (self.parent().postoji_projectil == False and self.game_over is False):
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
