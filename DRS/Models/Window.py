import datetime
import time

from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDesktopWidget, QLabel, QWidget, \
    QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
from Models.Player import Player
from Models.Projectile import Projectile
from Models.Alien import Alien
from Models.Health import Zivot
from Models.Stit import Stit
import random


class Window(QMainWindow):

    pomeri_dole_signal = pyqtSignal(int)
    pomeri_desno_signal = pyqtSignal(int)
    pomeri_levo_signal = pyqtSignal(int)

    player_kretanje_signal = pyqtSignal(list)
    projektil_kreiranje_signal = pyqtSignal(int)
    projektil_kretanje_signal = pyqtSignal(list)

    projektil_vanzemaljaca_kreiranje_signal = pyqtSignal()
    projektil_vanzemaljaca_kretanje_signal = pyqtSignal(int)

    nova_igra_signal = pyqtSignal(list)
    game_over_signal = pyqtSignal(int)

    sleep_signal = pyqtSignal()
    povratak_na_pocetak_signal = pyqtSignal()

    pokreni_vanzemaljce_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        ekran = QDesktopWidget().screenGeometry()
        self.razmera_sirina = ekran.width() / 1920
        self.razmera_visina = ekran.height() / 1080

        self.players = []
        self.aliens = []
        self.aliensZaPucanje = []
        self.lista_zivota = []
        self.lista_zivota2 = []
        self.stitovi = []
        self.projectiles = []
        self.projectiles.append(Projectile(self))
        self.projectiles.append(Projectile(self))
        #self.projectile2 = None
        self.postoji_projectils = []
        self.postoji_projectils.append(False)
        self.postoji_projectils.append(False)
        #self.postoji_projectil2 = False
        self.projectile_vanzemaljaca = None
        self.postoji_projectil_vanzemaljaca = False
        self.skor = 0
        self.skor2 = 0
        self.pogodio_playera = False
        self.ucitan_ui = False
        self.is_game_over = False

        self.pocetni_prozor()

    def pocetni_prozor(self):
        self.dugme_jedan_igrac = QPushButton('Jedan igrac', self)
        self.dugme_jedan_igrac.setStyleSheet('''QPushButton {color: white; border: 1px solid; border-color: white}QPushButton:hover {background-color: #328930;}''')
        self.dugme_jedan_igrac.setGeometry(280 * self.razmera_sirina, 300 * self.razmera_visina, 150 * self.razmera_sirina, 50 * self.razmera_visina)
        self.dugme_jedan_igrac.setFont(QFont('Ariel', 12))
        self.dugme_jedan_igrac.clicked.connect(self.jedan_igrac)
        self.dugme_jedan_igrac.setHidden(False)

        self.dugme_dva_igraca = QPushButton('Dva igraca', self)
        self.dugme_dva_igraca.setStyleSheet('''QPushButton {color: white; border: 1px solid; border-color: white}QPushButton:hover {background-color: #328930;}''')
        self.dugme_dva_igraca.setGeometry(280 * self.razmera_sirina, 400 * self.razmera_visina, 150 * self.razmera_sirina, 50 * self.razmera_visina)
        self.dugme_dva_igraca.setFont(QFont('Ariel', 12))
        self.dugme_dva_igraca.clicked.connect(self.dva_igraca)
        self.dugme_dva_igraca.setHidden(False)

        self.dugme_izadji = QPushButton('Izadji', self)
        self.dugme_izadji.setStyleSheet('''QPushButton {color: white; border: 1px solid; border-color: white}QPushButton:hover {background-color: #328930;}''')
        self.dugme_izadji.setGeometry(280 * self.razmera_sirina, 500 * self.razmera_visina, 150 * self.razmera_sirina, 50 * self.razmera_visina)
        self.dugme_izadji.setFont(QFont('Ariel', 12))
        self.dugme_izadji.clicked.connect(lambda:self.close())
        self.dugme_izadji.setHidden(False)

        self.setStyleSheet("background-color: black;")
        self.setWindowTitle("Space invader")
        self.setFixedSize(700 * self.razmera_sirina, 800 * self.razmera_visina)
        self.show()

    def jedan_igrac(self):
        self.nova_igra_signal.emit([0, 0])

        self.dugme_jedan_igrac.setHidden(True)
        self.dugme_dva_igraca.setHidden(True)
        self.dugme_izadji.setHidden(True)

        if self.ucitan_ui is False:
            self.players.append(Player(self))
            self.players.append(Player(self))
            self.players[0].dva_igraca = False
            self.players[1].dva_igraca = False
            self.set_ui()
            self.labela_skor2.setHidden(True)
            self.ucitan_ui = True
        else:
            self.labela_game_over.setHidden(True)
            self.labela_klikni_p.setHidden(True)
            self.labela_skor.setHidden(False)
            self.labela_skor2.setHidden(True)
            self.labela_izbor_igranja.setHidden(False)
            self.players[0].setHidden(False)
            self.players[1].setHidden(True)
            self.players[0].dva_igraca = False
            self.players[1].dva_igraca = False
            self.labela_skor.setHidden(False)
            self.players[0].game_on_signal.emit()
            self.players[0].setFocus()
            self.kretanje_vanzemaljca = kretanje_vanzemaljaca_thread(self)
            self.kretanje_vanzemaljca.start()

    def dva_igraca(self):
        self.nova_igra_signal.emit([0, 1])

        self.dugme_jedan_igrac.setHidden(True)
        self.dugme_dva_igraca.setHidden(True)
        self.dugme_izadji.setHidden(True)
        if self.ucitan_ui is False:
            self.players.append(Player(self))
            self.players.append(Player(self))
            self.players[0].dva_igraca = True
            self.players[1].dva_igraca = True
            self.set_ui()
            self.players[0].setFocus()
            self.ucitan_ui = True
        else:
            self.labela_game_over.setHidden(True)
            self.labela_klikni_p.setHidden(True)
            self.labela_skor.setHidden(False)
            self.labela_skor2.setHidden(False)
            self.labela_izbor_igranja.setHidden(False)
            self.players[0].setHidden(False)
            self.players[1].setHidden(False)
            self.players[0].dva_igraca = True
            self.players[1].dva_igraca = True
            self.players[0].game_on_signal.emit()
            self.players[1].game_on_signal.emit()
            self.players[0].setFocus()
            self.kretanje_vanzemaljca = kretanje_vanzemaljaca_thread(self)
            self.kretanje_vanzemaljca.start()

    def set_ui(self):
        self.labela_skor = QLabel(self)
        self.labela_skor.setFont(QFont('Arial', 13 * self.razmera_sirina))
        self.labela_skor.setText("SCORE: " + self.skor.__str__())
        self.labela_skor.setStyleSheet("color: white; font-weight: bold")
        self.labela_skor.setGeometry(20 * self.razmera_sirina, 30 * self.razmera_visina, 200 * self.razmera_sirina, 20 * self.razmera_visina)
        self.labela_skor.setHidden(False)

        self.labela_skor2 = QLabel(self)
        self.labela_skor2.setFont(QFont('Arial', 13 * self.razmera_sirina))
        self.labela_skor2.setText("SCORE: " + self.skor.__str__())
        self.labela_skor2.setStyleSheet("color: white; font-weight: bold")
        self.labela_skor2.setGeometry(580 * self.razmera_sirina, 30 * self.razmera_visina, 200 * self.razmera_sirina,
                                      20 * self.razmera_visina)
        self.labela_skor2.setHidden(False)


        self.labela_game_over = QLabel(self)
        self.labela_game_over.setFont(QFont('Arial', 13 * self.razmera_sirina))
        self.labela_game_over.setText("GAME OVER")
        self.labela_game_over.setStyleSheet("color: white; font-weight: bold")
        self.labela_game_over.setGeometry(300 * self.razmera_sirina, 30 * self.razmera_visina, 200 * self.razmera_sirina, 20 * self.razmera_visina)
        self.labela_game_over.setHidden(True)

        self.labela_klikni_p = QLabel(self)
        self.labela_klikni_p.setFont(QFont('Arial', 13 * self.razmera_sirina))
        self.labela_klikni_p.setText("Klikni P za novu igru !")
        self.labela_klikni_p.setStyleSheet("color: white; font-weight: bold")
        self.labela_klikni_p.setGeometry(260 * self.razmera_sirina, 100 * self.razmera_visina, 220 * self.razmera_sirina, 30 * self.razmera_visina)
        self.labela_klikni_p.setHidden(True)

        self.pomeri_dole_signal.connect(self.pomeranje_dole)
        self.pomeri_desno_signal.connect(self.pomeranje_desno)
        self.pomeri_levo_signal.connect(self.pomeranje_levo)

        self.player_kretanje_signal.connect(self.pomeranje_igraca)
        self.projektil_kreiranje_signal.connect(self.kreiranje_projektila)
        self.projektil_kretanje_signal.connect(self.kretanje_projektila)

        self.kretanje_vanzemaljca = kretanje_vanzemaljaca_thread(self)

        self.projektil_vanzemaljaca_kreiranje_signal.connect(self.kreiranje_projektila_vanzemaljaca)
        self.projektil_vanzemaljaca_kretanje_signal.connect(self.kretanje_projektila_vanzemaljaca)

        self.nova_igra_signal.connect(self.nova_igra)
        self.game_over_signal.connect(self.game_over)

        self.sleep_signal.connect(self.sleepp)
        self.povratak_na_pocetak_signal.connect(self.povratak_na_pocetni_prozor)

        self.pokreni_vanzemaljce_signal.connect(self.pokreni_vanzemaljce)

        if self.players[0].dva_igraca:
            self.layout().addWidget(self.players[0])
            self.players[0].move(100 * self.razmera_sirina, 700 * self.razmera_visina)
            self.players[0].setFocus()
            self.layout().addWidget(self.players[1])
            self.players[1].move(550 * self.razmera_sirina, 700 * self.razmera_visina)
            self.players[1].setFocus()
        else:
            self.layout().addWidget(self.players[0])
            self.players[0].move(300 * self.razmera_sirina, 700 * self.razmera_visina)
            self.players[0].setFocus()

        #self.layout().addWidget(self.players[1])
        #self.players[1].move(300 * self.razmera_sirina, 700 * self.razmera_visina)

        self.kreiranje_vanzemaljaca()
        self.kreiranje_zivota()
        if self.players[0].dva_igraca:
            self.kreiranje_zivota2()
        self.kreiranje_stita()

        self.kretanje_vanzemaljca = kretanje_vanzemaljaca_thread(self)
        self.kretanje_vanzemaljca.start()

    def closeEvent(self, event):
        self.players[0].game_over_signal.emit()
        self.players[1].game_over_signal.emit()

        self.kretanje_vanzemaljca.gasenje_signal.emit()
        self.kretanje_vanzemaljca.wait(1000)
        self.kretanje_vanzemaljca.terminate()

        if(self.postoji_projectil_vanzemaljaca == True):
            self.projektil_vanzemaljaca_kretanje.gasenje_signal.emit()
            self.projektil_vanzemaljaca_kretanje.wait(1000)
            self.projektil_vanzemaljaca_kretanje.terminate()

        if(self.postoji_projectils[0] == True):
            self.projektil_kretanje.gasenje_signal.emit()
            self.projektil_kretanje.wait(1000)
            self.projektil_kretanje.terminate()
        if (self.postoji_projectils[1] == True):
            self.projektil_kretanje2.gasenje_signal.emit()
            self.projektil_kretanje2.wait(1000)
            self.projektil_kretanje2.terminate()

    def povratak_na_pocetni_prozor(self):
        self.is_game_over = False

        for i in self.stitovi:
            i.setParent(None)
            self.layout().removeWidget(i)
        self.stitovi.clear()

        for i in self.aliens:
            i.setParent(None)
            self.layout().removeWidget(i)

        for i in self.lista_zivota:
            i.setParent(None)
            self.layout().removeWidget(i)

        for i in self.lista_zivota2:
            i.setParent(None)
            self.layout().removeWidget(i)

        self.aliensZaPucanje.clear()
        self.aliens.clear()

        self.labela_game_over.setHidden(True)
        self.labela_klikni_p.setHidden(True)
        self.labela_skor.setHidden(True)
        self.labela_skor2.setHidden(True)

        self.players[0].setHidden(True)
        self.players[1].setHidden(True)

        self.dugme_jedan_igrac.setHidden(False)
        self.dugme_dva_igraca.setHidden(False)
        self.dugme_izadji.setHidden(False)

    @pyqtSlot()
    def sleepp(self):
        self.labela_game_over.setHidden(True)
        self.labela_game_over.setText("GAME OVER")
        self.labela_klikni_p.setHidden(True)

        self.kretanje_vanzemaljca = kretanje_vanzemaljaca_thread(self)
        self.kretanje_vanzemaljca.start()

    @pyqtSlot(int)   # 0 - game over, 1 - novi nivo
    def game_over(self, novi_nivo):
        self.kretanje_vanzemaljca.gasenje_signal.emit()

        for i in range(2):
            if self.postoji_projectils[i]:
                if i == 0:
                    self.projektil_kretanje.gasenje_signal.emit()
                else:
                    self.projektil_kretanje2.gasenje_signal.emit()
                self.postoji_projectils[i] = False
                self.projectiles[i].setParent(None)


        if self.postoji_projectil_vanzemaljaca:
            self.projektil_vanzemaljaca_kretanje.gasenje_signal.emit()
            self.postoji_projectil_vanzemaljaca = False
            self.projectile_vanzemaljaca.setParent(None)


        if(novi_nivo == 0):
            self.players[0].game_over_signal.emit(0)
            self.labela_game_over.setHidden(False)
            self.labela_klikni_p.setHidden(True)

            self.is_game_over = True
            self.spavanje = sleep_thread(self)
            self.spavanje.start()

        if(self.players[0].dva_igraca == True):
            if(novi_nivo == 1):
                self.nova_igra_signal.emit([1, 1])
        else:
            if (novi_nivo == 1):
                self.nova_igra_signal.emit([1, 0])

    def pokreni_vanzemaljce(self):
        self.kretanje_vanzemaljca.start()

    @pyqtSlot(list)    #novi_nivo[0] - game over(0) ili novi nivo(1), novi_nivo[1] - jedan(0) ili dva(1) igraca
    def nova_igra(self, novi_nivo):
        if(novi_nivo[0] == 0 or novi_nivo[0] == 3):
            self.skor = 0
            self.labela_skor.setText("SCORE: " + self.skor.__str__())
            self.skor2 = 0
            self.labela_skor2.setText("SCORE: " + self.skor2.__str__())

        if novi_nivo[1] == 1:
            self.players[0].move(100 * self.razmera_sirina, 700 * self.razmera_visina)
            self.players[1].move(550 * self.razmera_sirina, 700 * self.razmera_visina)
        else:
            self.players[0].move(300 * self.razmera_sirina, 700 * self.razmera_visina)

        for i in self.stitovi:
            i.setParent(None)
            self.layout().removeWidget(i)

        self.stitovi.clear()
        self.kreiranje_stita()

        if(novi_nivo[0] == 0 or novi_nivo[0] == 3):
            for i in self.lista_zivota:
                i.setParent(None)
                self.layout().removeWidget(i)
            self.lista_zivota.clear()
            self.kreiranje_zivota()
            for i in self.lista_zivota2:
                i.setParent(None)
                self.layout().removeWidget(i)
            self.lista_zivota2.clear()
            if novi_nivo[1] == 1:
                self.kreiranje_zivota2()

        for i in self.aliens:
            i.setParent(None)
            self.layout().removeWidget(i)

        self.aliensZaPucanje.clear()
        self.aliens.clear()
        self.kreiranje_vanzemaljaca()

        if (novi_nivo[0] == 1):
            self.labela_game_over.setText("NOVI NIVO")
            self.labela_game_over.setHidden(False)
            self.spavanje = sleep_thread(self)
            self.spavanje.start()

        if novi_nivo[0] == 0:
            self.labela_game_over.setHidden(True)
            self.labela_klikni_p.setHidden(True)

            self.kretanje_vanzemaljca = kretanje_vanzemaljaca_thread(self)


    @pyqtSlot(int)
    def pomeranje_dole(self, i):
        self.aliens[i].move(self.aliens[i].x(), self.aliens[i].y() + 20 * self.razmera_visina)

    @pyqtSlot(int)
    def pomeranje_desno(self, i):
        self.aliens[i].move(self.aliens[i].x() + 15 * self.razmera_sirina, self.aliens[i].y())

    @pyqtSlot(int)
    def pomeranje_levo(self, i):
        self.aliens[i].move(self.aliens[i].x() - 15 * self.razmera_sirina, self.aliens[i].y())

    @pyqtSlot(list)    #params[0] - desno(0) ili levo(1), params[1] - igrac 1(0) ili 2(1)
    def pomeranje_igraca(self, params):
        if params[0] == 0:
            if self.players[params[1]].x() <= self.razmera_sirina * 650:
                self.players[params[1]].move(self.players[params[1]].x() + 10 * self.razmera_sirina, self.players[params[1]].y())
        else:
            if self.players[params[1]].x() >= self.razmera_sirina * 10:
                self.players[params[1]].move(self.players[params[1]].x() - 10 * self.razmera_sirina, self.players[params[1]].y())

    @pyqtSlot(int)  #index == 0 - prvi igrac, index == 1 - drugi igrac
    def kreiranje_projektila(self, index):
        projectile = Projectile(self)
        self.projectiles[index] = projectile
        self.postoji_projectils[index] = True
        self.layout().addWidget(self.projectiles[index])
        projectile.move(self.players[index].x() + 21 * self.razmera_sirina,
                        self.players[index].y() - 5 * self.razmera_visina)
        if index == 0:
            self.projektil_kretanje = kretanje_projektila_thread(self, self.projectiles[index], index)
            self.projektil_kretanje.start()
        elif index == 1:
            self.projektil_kretanje2 = kretanje_projektila_thread(self, self.projectiles[index], index)
            self.projektil_kretanje2.start()


    def kreiranje_stita(self):
        stit = Stit(self)
        self.layout().addWidget(stit)
        stit.move(60 * self.razmera_sirina, 600 * self.razmera_visina)
        self.stitovi.append(stit)
        stit = Stit(self)
        self.layout().addWidget(stit)
        stit.move(180 * self.razmera_sirina, 600 * self.razmera_visina)
        self.stitovi.append(stit)
        stit = Stit(self)
        self.layout().addWidget(stit)
        stit.move(310 * self.razmera_sirina, 600 * self.razmera_visina)
        self.stitovi.append(stit)
        stit = Stit(self)
        self.layout().addWidget(stit)
        stit.move(440 * self.razmera_sirina, 600 * self.razmera_visina)
        self.stitovi.append(stit)
        stit = Stit(self)
        self.layout().addWidget(stit)
        stit.move(560 * self.razmera_sirina, 600 * self.razmera_visina)
        self.stitovi.append(stit)

    @pyqtSlot(list)     #params[0] - dali je dosao do kraja(0) u suprotnom (1), params[1] - indeks projektila koji igrac ga je kreirao
    def kretanje_projektila(self, params):
        if params[0] == 0:
            self.projectiles[params[1]].move(self.projectiles[params[1]].x(), 0)
            self.projectiles[params[1]].setParent(None)
            self.postoji_projectils[params[1]] = False
        else:
            self.projectiles[params[1]].move(self.projectiles[params[1]].x(), self.projectiles[params[1]].y() - 20 * self.razmera_visina)

        if self.postoji_projectils[params[1]]:
            for i in reversed(self.aliens):
                if i.postoji:
                    if (self.projectiles[params[1]].y() >= i.y() and self.projectiles[params[1]].y() <= i.y() + 20 * self.razmera_visina) and (
                            self.projectiles[params[1]].x() >= i.x() and self.projectiles[params[1]].x() <= i.x() + 30 * self.razmera_visina):
                        self.aliens[self.aliens.index(i)].postoji = False
                        i.setParent(None)
                        self.aliensZaPucanje.remove(i)
                        self.projectiles[params[1]].setParent(None)
                        self.postoji_projectils[params[1]] = False
                        if params[1] == 0:
                            self.skor += 1
                            self.labela_skor.setText("SCORE: " + self.skor.__str__())
                            self.projektil_kretanje.gasenje_signal.emit()
                        elif params[1] == 1:
                            self.skor2 += 1
                            self.labela_skor2.setText("SCORE: " + self.skor2.__str__())
                            self.projektil_kretanje2.gasenje_signal.emit()
                        if len(self.aliensZaPucanje) == 0:
                            self.game_over_signal.emit(1)
                        break


        if(self.postoji_projectil_vanzemaljaca != False):
            if(self.projectiles[params[1]].y() >= self.projectile_vanzemaljaca.y() and self.projectiles[params[1]].y() <= self.projectile_vanzemaljaca.y() + 10 * self.razmera_visina) and \
                            (self.projectiles[params[1]].x() >= self.projectile_vanzemaljaca.x() and self.projectiles[params[1]].x() <= self.projectile_vanzemaljaca.x() + 10 * self.razmera_visina):
                self.projectiles[params[1]].setParent(None)
                self.postoji_projectils[params[1]] = False
                if params[1] == 0:
                    self.projektil_kretanje.gasenje_signal.emit()
                else:
                    self.projektil_kretanje2.gasenje_signal.emit()
                self.projectile_vanzemaljaca.setParent(None)
                self.postoji_projectil_vanzemaljaca = False
                self.projektil_vanzemaljaca_kretanje.gasenje_signal.emit()

        if (self.postoji_projectils[params[1]]):
            for i in self.stitovi:
                if (self.projectiles[params[1]].y() >= i.y() and self.projectiles[params[1]].y() <= i.y() + 50 * self.razmera_visina) and (
                        self.projectiles[params[1]].x() >= i.x() and self.projectiles[params[1]].x() <= i.x() + 70 * self.razmera_visina):
                    if (i.nivo_ostecenja == 0):
                        slika_stita = QPixmap("Ostecenje_1.png")
                        i.setPixmap(slika_stita.scaled(70 * self.razmera_sirina, 50 * self.razmera_visina))
                        i.nivo_ostecenja += 1
                    elif (i.nivo_ostecenja == 1):
                        slika_stita = QPixmap("Ostecenje_2.png")
                        i.setPixmap(slika_stita.scaled(70 * self.razmera_sirina, 50 * self.razmera_visina))
                        i.nivo_ostecenja += 1
                    elif (i.nivo_ostecenja == 2):
                        slika_stita = QPixmap("Ostecenje_3.png")
                        i.setPixmap(slika_stita.scaled(70 * self.razmera_sirina, 50 * self.razmera_visina))
                        i.nivo_ostecenja += 1
                    elif (i.nivo_ostecenja == 3):
                        slika_stita = QPixmap("Ostecenje_4.png")
                        i.setPixmap(slika_stita.scaled(70 * self.razmera_sirina, 50 * self.razmera_visina))
                        i.nivo_ostecenja += 1
                    else:
                        i.setParent(None)
                        self.stitovi.remove(i)
                    if params[1] == 0:
                        self.projektil_kretanje.gasenje_signal.emit()
                    else:
                        self.projektil_kretanje2.gasenje_signal.emit()
                    self.projectiles[params[1]].setParent(None)
                    self.postoji_projectils[params[1]] = False
                    break


    @pyqtSlot()
    def kreiranje_projektila_vanzemaljaca(self):
        projectile = Projectile(self, 10, 10, "pow.png")
        self.projectile_vanzemaljaca = projectile
        self.postoji_projectil_vanzemaljaca = True
        alien = random.choice(self.aliensZaPucanje)
        for i in range(self.aliensZaPucanje.index(alien), len(self.aliensZaPucanje)):
            if(alien.red == 5):
                break
            if(alien.kolona == self.aliensZaPucanje[i].kolona and alien.red < self.aliensZaPucanje[i].red):
                alien = self.aliensZaPucanje[i]
        self.layout().addWidget(self.projectile_vanzemaljaca)
        projectile.move(alien.x() + 10 * self.razmera_sirina, alien.y() + 25 * self.razmera_visina)
        self.projektil_vanzemaljaca_kretanje = kretanje_projektila_vanzemaljaca_thread(self, self.projectile_vanzemaljaca)
        self.projektil_vanzemaljaca_kretanje.start()

    @pyqtSlot(int)
    def kretanje_projektila_vanzemaljaca(self, i):
        if i == 0:
            self.projectile_vanzemaljaca.move(self.projectile_vanzemaljaca.x(), 800 * self.razmera_visina)
            self.projectile_vanzemaljaca.setParent(None)
            self.postoji_projectil_vanzemaljaca = False
        else:
            self.projectile_vanzemaljaca.move(self.projectile_vanzemaljaca.x(), self.projectile_vanzemaljaca.y() + 10 * self.razmera_visina)

        for index in range(2):
            if (self.projectile_vanzemaljaca.x() >= self.players[index].x() and self.projectile_vanzemaljaca.x() <= self.players[index].x() + 45 * self.razmera_visina) and \
                    (self.projectile_vanzemaljaca.y() >= self.players[index].y() and self.projectile_vanzemaljaca.y() <= self.players[index].y() + 70 * self.razmera_visina):
                if self.postoji_projectil_vanzemaljaca:
                    if index == 0:
                        for i in self.lista_zivota:
                            if i.postoji:
                                i.setParent(None)
                                self.lista_zivota[self.lista_zivota.index(i)].postoji = False
                                self.lista_zivota.remove(i)
                                self.projectile_vanzemaljaca.setParent(None)
                                if(len(self.lista_zivota) == 0):
                                    self.players[index].game_over_signal.emit(0)
                                    self.players[index].setHidden(True)
                                self.postoji_projectil_vanzemaljaca = False
                                self.projektil_vanzemaljaca_kretanje.gasenje_signal.emit()
                                break
                    elif index == 1:
                        for i in self.lista_zivota2:
                            if i.postoji:
                                i.setParent(None)
                                self.lista_zivota2[self.lista_zivota2.index(i)].postoji = False
                                self.lista_zivota2.remove(i)
                                if (len(self.lista_zivota2) == 0):
                                    self.players[0].game_over_signal.emit(1)
                                    self.players[index].setHidden(True)
                                self.projectile_vanzemaljaca.setParent(None)
                                self.postoji_projectil_vanzemaljaca = False
                                self.projektil_vanzemaljaca_kretanje.gasenje_signal.emit()
                                break

                    if self.players[0].dva_igraca is False:
                        if len(self.lista_zivota) == 0:
                            self.game_over_signal.emit(0)
                    else:
                        if len(self.lista_zivota) + len(self.lista_zivota2) == 0:
                            self.game_over_signal.emit(0)

        if (self.postoji_projectil_vanzemaljaca):
            for i in self.stitovi:
                if (self.projectile_vanzemaljaca.y() >= i.y() and self.projectile_vanzemaljaca.y() <= i.y() + 60 * self.razmera_visina) and (
                        self.projectile_vanzemaljaca.x() >= i.x() and self.projectile_vanzemaljaca.x() <= i.x() + 80 * self.razmera_visina):
                    if (i.nivo_ostecenja == 0):
                        slika_stita = QPixmap("Ostecenje_1.png")
                        i.setPixmap(slika_stita.scaled(80 * self.razmera_sirina, 60 * self.razmera_visina))
                        i.nivo_ostecenja += 1
                    elif (i.nivo_ostecenja == 1):
                        slika_stita = QPixmap("Ostecenje_2.png")
                        i.setPixmap(slika_stita.scaled(80 * self.razmera_sirina, 60 * self.razmera_visina))
                        i.nivo_ostecenja += 1
                    elif (i.nivo_ostecenja == 2):
                        slika_stita = QPixmap("Ostecenje_3.png")
                        i.setPixmap(slika_stita.scaled(80 * self.razmera_sirina, 60 * self.razmera_visina))
                        i.nivo_ostecenja += 1
                    elif (i.nivo_ostecenja == 3):
                        slika_stita = QPixmap("Ostecenje_4.png")
                        i.setPixmap(slika_stita.scaled(80 * self.razmera_sirina, 60 * self.razmera_visina))
                        i.nivo_ostecenja += 1
                    else:
                        i.setParent(None)
                        self.stitovi.remove(i)
                    self.projektil_vanzemaljaca_kretanje.gasenje_signal.emit()
                    self.projectile_vanzemaljaca.setParent(None)
                    self.postoji_projectil_vanzemaljaca = False
                    break

    def kreiranje_vanzemaljaca(self):
        slika = "alien2.png"
        red = 1
        kolona = 1
        for i in range(55):
            if i == 0:
                alien = Alien(slika, red, kolona, self)
                self.layout().addWidget(alien)
                alien.move(70 * self.razmera_sirina, 200 * self.razmera_visina)
                self.aliens.append(alien)
                self.aliensZaPucanje.append(alien)
            elif i != 0 and i % 11 == 0:
                red += 1
                kolona = 1
                if red == 2 or red == 3:
                    slika = "alien.png"
                else:
                    slika = "alien3.png"
                alien = Alien(slika, red, kolona, self)
                self.layout().addWidget(alien)
                alien.move(self.aliens[i-11].x(), self.aliens[i-11].y() + 40 * self.razmera_visina)
                self.aliens.append(alien)
                self.aliensZaPucanje.append(alien)
            else:
                kolona += 1
                alien = Alien(slika, red, kolona, self)
                self.layout().addWidget(alien)
                alien.move(self.aliens[i-1].x() + 50 * self.razmera_sirina, self.aliens[i-1].y())
                self.aliens.append(alien)
                self.aliensZaPucanje.append(alien)



    def kreiranje_zivota(self):
        zivot = Zivot(self)
        self.layout().addWidget(zivot)
        zivot.move(20 * self.razmera_sirina, 60 * self.razmera_visina)
        self.lista_zivota.append(zivot)

        zivot = Zivot(self)
        self.layout().addWidget(zivot)
        zivot.move(60 * self.razmera_sirina, 60 * self.razmera_visina)
        self.lista_zivota.append(zivot)

        zivot = Zivot(self)
        self.layout().addWidget(zivot)
        zivot.move(100 * self.razmera_sirina, 60 * self.razmera_visina)
        self.lista_zivota.append(zivot)

    def kreiranje_zivota2(self):
        zivot = Zivot(self)
        self.layout().addWidget(zivot)
        zivot.move(580 * self.razmera_sirina, 60 * self.razmera_visina)
        self.lista_zivota2.append(zivot)

        zivot = Zivot(self)
        self.layout().addWidget(zivot)
        zivot.move(620 * self.razmera_sirina, 60 * self.razmera_visina)
        self.lista_zivota2.append(zivot)

        zivot = Zivot(self)
        self.layout().addWidget(zivot)
        zivot.move(660 * self.razmera_sirina, 60 * self.razmera_visina)
        self.lista_zivota2.append(zivot)

class sleep_thread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        time.sleep(2)
        if self.parent().is_game_over:
            self.parent().povratak_na_pocetak_signal.emit()
        else:
            self.parent().sleep_signal.emit()

class kretanje_vanzemaljaca_thread(QThread):

    gasenje_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.gasenje = False
        self.gasenje_signal.connect(self.izlaz)

    @pyqtSlot()
    def izlaz(self):
        self.gasenje = True

    def run(self):
        kretanje_desno = False
        dosao_do_ivice = False
        nova_iteracija = False
        izvrseno_pomeranje_dole = False
        izvrseno_pomeranje_dole_za_vreme = False

        korak = 11

        spavanje_niti = 1
        broj_zivih = len(self.parent().aliensZaPucanje)
        vreme_za_pucanje = 0
        granica_za_pucanje = 1

        vreme_izvrsenja = 0.3

        while self.gasenje is False:
            if broj_zivih <= 55 and broj_zivih > 45:
                spavanje_niti = 1.3 - vreme_izvrsenja
            if broj_zivih <= 45 and broj_zivih > 34:
                spavanje_niti = 1.1 - vreme_izvrsenja
            elif broj_zivih <= 34 and broj_zivih > 23:
                spavanje_niti = 0.9 - vreme_izvrsenja
            elif broj_zivih <= 23 and broj_zivih > 12:
                spavanje_niti = 0.8 - vreme_izvrsenja
            elif broj_zivih <= 12 and broj_zivih > 6:
                granica_za_pucanje = 0.6
                spavanje_niti = 0.6 - vreme_izvrsenja
            elif broj_zivih <= 6 and broj_zivih > 2:
                granica_za_pucanje = 0.4
                spavanje_niti = 0.5 - vreme_izvrsenja
            elif broj_zivih == 2:
                spavanje_niti = 0.4 - vreme_izvrsenja
            elif broj_zivih == 1:
                granica_za_pucanje = 0.5
                spavanje_niti = 0.2 - vreme_izvrsenja

            if nova_iteracija == False:
                time.sleep(spavanje_niti)
                vreme_za_pucanje += spavanje_niti
            br = 0
            pocetak = datetime.datetime.now()

            indexVanzemaljca = -1
            pronadjenIndexVanzemaljca = False
            brojProlaza = 0

            while(pronadjenIndexVanzemaljca is False and len(self.parent().aliensZaPucanje) != 0):
                indexProvere = (len(self.parent().aliens) - 1)

                if kretanje_desno is False:
                    indexProvere -= 10
                    indexProvere += brojProlaza
                else:
                    indexProvere -= brojProlaza

                for i in range(5):
                    if (self.parent().aliens[indexProvere].postoji):
                        indexVanzemaljca = indexProvere
                        pronadjenIndexVanzemaljca = True
                        break
                    else:
                        indexProvere -= korak

                brojProlaza += 1
            if len(self.parent().aliensZaPucanje) == 0:
                continue

            if nova_iteracija and dosao_do_ivice:
                for i in reversed(self.parent().aliens):
                    self.parent().pomeri_dole_signal.emit(self.parent().aliens.index(i))
                    br += 1
                    if br % 11 == 0:
                        time.sleep(0.05 * spavanje_niti)
            elif kretanje_desno:
                if self.parent().aliens[indexVanzemaljca].x() + 50 * self.parent().razmera_sirina <= 650 * self.parent().razmera_sirina:
                    for i in reversed(self.parent().aliens):
                        self.parent().pomeri_desno_signal.emit(self.parent().aliens.index(i))
                        br += 1
                        if br % 11 == 0:
                            time.sleep(0.05 * spavanje_niti)
                else:
                    kretanje_desno = False
                    dosao_do_ivice = True
            else:
                if self.parent().aliens[indexVanzemaljca].x() - 50 * self.parent().razmera_sirina >= 0:
                    for i in reversed(self.parent().aliens):
                        self.parent().pomeri_levo_signal.emit(self.parent().aliens.index(i))
                        br += 1
                        if br % 11 == 0:
                            time.sleep(0.05 * spavanje_niti)
                else:
                    kretanje_desno = True
                    dosao_do_ivice = True

            if dosao_do_ivice and nova_iteracija:
                izvrseno_pomeranje_dole = True
                izvrseno_pomeranje_dole_za_vreme = True

            if dosao_do_ivice and izvrseno_pomeranje_dole is False:
                nova_iteracija = True
            else:
                nova_iteracija = False
                dosao_do_ivice = False
                izvrseno_pomeranje_dole = False

            dosao_do_dna = False

            if dosao_do_ivice:
                for i in reversed(self.parent().aliens):
                    if i.postoji:
                        if len(self.parent().stitovi) != 0:
                            if i.y() > 560 * self.parent().razmera_visina:
                                dosao_do_dna = True
                                self.parent().game_over_signal.emit(0)
                                break
                        else:
                            if i.y() > 640 * self.parent().razmera_visina:
                                dosao_do_dna = True
                                self.parent().game_over_signal.emit(0)
                                break

            if dosao_do_dna:
                break

            if vreme_za_pucanje >= granica_za_pucanje and self.gasenje is False:
                if self.parent().postoji_projectil_vanzemaljaca is False:
                    self.parent().projektil_vanzemaljaca_kreiranje_signal.emit()
                    vreme_za_pucanje = 0

            broj_zivih = len(self.parent().aliensZaPucanje)

            if izvrseno_pomeranje_dole_za_vreme is False:
                kraj = datetime.datetime.now()
                vreme_izvrsenja = (pocetak - kraj).total_seconds() * -1
            else:
                izvrseno_pomeranje_dole_za_vreme = False


class kretanje_projektila_thread(QThread):

    gasenje_signal = pyqtSignal()

    def __init__(self, parent=None, projectile=None, index=None):
        super().__init__(parent)
        self.projectile = projectile
        self.index = index
        self.gasenje = False
        self.gasenje_signal.connect(self.izlaz)

    @pyqtSlot()
    def izlaz(self):
        self.gasenje = True

    def run(self):
        while self.projectile.y() > 0 and self.gasenje is False:
            time.sleep(0.03)
            if self.projectile.y() < 100 * self.parent().razmera_visina and self.projectile.y() > 0:
                self.parent().projektil_kretanje_signal.emit([0, self.index])
                break
            else:
                self.parent().projektil_kretanje_signal.emit([1, self.index])


class kretanje_projektila_vanzemaljaca_thread(QThread):

    gasenje_signal = pyqtSignal()

    def __init__(self, parent=None, projectile=None):
        super().__init__(parent)
        self.projectile = projectile
        self.gasenje = False
        self.gasenje_signal.connect(self.izlaz)

    @pyqtSlot()
    def izlaz(self):
        self.gasenje = True

    def run(self):
        while self.projectile.y() > 0 and self.gasenje is False:
            time.sleep(0.05)
            if self.projectile.y() > 750 * self.parent().razmera_visina and self.projectile.y() < 800 * self.parent().razmera_visina:
                self.parent().projektil_vanzemaljaca_kretanje_signal.emit(0)
                break
            else:
                self.parent().projektil_vanzemaljaca_kretanje_signal.emit(1)
