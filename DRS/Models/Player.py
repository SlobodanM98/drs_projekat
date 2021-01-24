import time
from threading import Thread

from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDesktopWidget, QWidget, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5 import QtGui
import sys


class Player(QLabel):

    game_over_signal = pyqtSignal(int)
    game_on_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        slika = QPixmap("rocket.png")
        self.setPixmap(slika.scaled(45 * self.parent().razmera_sirina, 70 * self.parent().razmera_visina))
        self.resize(50 * self.parent().razmera_sirina, 70 * self.parent().razmera_visina)
        self.keylist = []
        self.keys = []
        self.a_odpusteno = False
        self.d_odpusteno = False
        self.leva_strelica_odpusteno = False
        self.desna_strelica_odpusteno = False
        self.game_over = False
        self.dva_igraca = False
        self.blokiran_drugi = False
        self.blokiran = False
        self.game_over_signal.connect(self.gasenje)
        self.game_on_signal.connect(self.paljenje)

    @pyqtSlot(int)
    def gasenje(self, i):
        if i == 0:
            self.game_over = True
        elif i == 1:
            self.blokiran_drugi = True


    def paljenje(self):
        self.game_over = False
        #self.izabrano_kretanje = False
        self.a_odpusteno = False
        self.d_odpusteno = False
        self.leva_strelica_odpusteno = False
        self.desna_strelica_odpusteno = False
        #self.na_strelice = False

    def keyPressEvent(self, event):
        if self.game_over is False:
            if event.key() == Qt.Key_A:
                nit = Thread(target=self.pritisnutoA, args=[0])
                nit.start()
            if event.key() == Qt.Key_D:
                nit = Thread(target=self.pritisnutoD, args=[0])
                nit.start()
            if event.key() == Qt.Key_Space:
                nit = Thread(target=self.pritisnut_space, args=[0])
                nit.start()
        if self.dva_igraca:
            if self.blokiran_drugi is False:
                if event.key() == Qt.Key_Right:
                    nit2 = Thread(target=self.pritisnutoD, args=[1])
                    nit2.start()
                if event.key() == Qt.Key_Left:
                    nit2 = Thread(target=self.pritisnutoA, args=[1])
                    nit2.start()
                if (event.key() == Qt.Key_Enter):
                    nit = Thread(target=self.pritisnut_space, args=[1])
                    nit.start()

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
        if event.key() == Qt.Key_A:
            self.a_odpusteno = True
        if event.key() == Qt.Key_D:
            self.d_odpusteno = True
        if event.key() == Qt.Key_Space:
            self.space_odpusteno = True
        if self.dva_igraca:
            if event.key() == Qt.Key_Right:
                self.desna_strelica_odpusteno = True
            if event.key() == Qt.Key_Left:
                self.leva_strelica_odpusteno = True





    def pritisnut_space(self, pritisnuto):
        if pritisnuto == 0:
            if (self.parent().postoji_projectils[0] == False):
                self.parent().projektil_kreiranje_signal.emit(0)
        elif pritisnuto == 1:
            if (self.parent().postoji_projectils[1] == False):
                self.parent().projektil_kreiranje_signal.emit(1)


    def pritisnutoA(self, pritisnuto):   #pritisnuto = 0 - pritisbuto a, pritisnuto = 1 - pritisnuta strelica
        if pritisnuto == 0:
            while self.a_odpusteno != True:
                self.parent().player_kretanje_signal.emit([1, 0])
                time.sleep(0.05)

            self.a_odpusteno = False
        elif pritisnuto == 1:
            while self.leva_strelica_odpusteno != True:
                self.parent().player_kretanje_signal.emit([1, 1])
                time.sleep(0.05)

            self.leva_strelica_odpusteno = False


    def pritisnutoD(self, pritisnuto):
        if pritisnuto == 0:
            while self.d_odpusteno != True:
                self.parent().player_kretanje_signal.emit([0, 0])
                time.sleep(0.05)

            self.d_odpusteno = False
        elif pritisnuto == 1:
            while self.desna_strelica_odpusteno != True:
                self.parent().player_kretanje_signal.emit([0, 1])
                time.sleep(0.05)

            self.desna_strelica_odpusteno = False
