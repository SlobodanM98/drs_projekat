import time

from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDesktopWidget, QLabel, QWidget, \
    QHBoxLayout, QVBoxLayout
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

    player_kretanje_signal = pyqtSignal(int)
    projektil_kreiranje_signal = pyqtSignal()
    projektil_kretanje_signal = pyqtSignal(int)

    projektil_vanzemaljaca_kreiranje_signal = pyqtSignal()
    projektil_vanzemaljaca_kretanje_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.player = Player(self)
        self.aliens = []
        self.aliensZaPucanje = []
        self.lista_zivota = []
        self.lista_preostalih_zivota = []
        self.stitovi = []
        self.projectile = None
        self.postoji_projectil = False
        self.projectile_vanzemaljaca = None
        self.postoji_projectil_vanzemaljaca = False
        self.skor = 0
        self.pogodio_playera = False

        self.set_ui()

    def set_ui(self):
        self.setStyleSheet("background-color: black;")
        vbox = QVBoxLayout(self)

        self.labela_skor = QLabel(self)
        self.labela_skor.setFont(QFont('Arial', 13))
        self.labela_skor.setText("SCORE: " + self.skor.__str__())
        self.labela_skor.setStyleSheet("color: white; font-weight: bold")
        self.labela_skor.move(self.x()+20, self.y() + 20)

        self.pomeri_dole_signal.connect(self.pomeranje_dole)
        self.pomeri_desno_signal.connect(self.pomeranje_desno)
        self.pomeri_levo_signal.connect(self.pomeranje_levo)

        self.player_kretanje_signal.connect(self.pomeranje_igraca)
        self.projektil_kreiranje_signal.connect(self.kreiranje_projektila)
        self.projektil_kretanje_signal.connect(self.kretanje_projektila)

        self.kretanje_vanzemaljca = kretanje_vanzemaljaca_thread(self)

        self.projektil_vanzemaljaca_kreiranje_signal.connect(self.kreiranje_projektila_vanzemaljaca)
        self.projektil_vanzemaljaca_kretanje_signal.connect(self.kretanje_projektila_vanzemaljaca)

        self.setFixedSize(700, 800)
        vbox.addWidget(self.player)
        self.player.move(300, 700)
        self.player.setFocus()

        self.kreiranje_vanzemaljaca(vbox)
        self.kreiranje_zivota(vbox)

        self.kreiranje_stita()

        self.kretanje_vanzemaljca.start()

        self.setLayout(vbox)
        self.setGeometry(600, 100, 500, 500)
        self.setWindowTitle("Space invader")
        self.show()

    @pyqtSlot(int)
    def pomeranje_dole(self, i):
        self.aliens[i].move(self.aliens[i].x(), self.aliens[i].y() + 20)

    @pyqtSlot(int)
    def pomeranje_desno(self, i):
        self.aliens[i].move(self.aliens[i].x() + 10, self.aliens[i].y())

    @pyqtSlot(int)
    def pomeranje_levo(self, i):
        self.aliens[i].move(self.aliens[i].x() - 10, self.aliens[i].y())

    @pyqtSlot(int)
    def pomeranje_igraca(self, i):
        if i == 0:
            self.player.move(self.player.x() + 10, self.player.y())
        else:
            self.player.move(self.player.x() - 10, self.player.y())

    @pyqtSlot()
    def kreiranje_projektila(self):
        projectile = Projectile(self)
        self.projectile = projectile
        self.postoji_projectil = True
        self.layout().addWidget(self.projectile)
        projectile.move(self.player.x() + 21, self.player.y() - 5)
        self.projektil_kretanje = kretanje_projektila_thread(self, self.projectile)
        self.projektil_kretanje.start()

    def kreiranje_stita(self):
        stit = Stit(self)
        self.layout().addWidget(stit)
        stit.move(100, 470)
        self.stitovi.append(stit)
        stit = Stit(self)
        self.layout().addWidget(stit)
        stit.move(300, 470)
        self.stitovi.append(stit)
        stit = Stit(self)
        self.layout().addWidget(stit)
        stit.move(500, 470)
        self.stitovi.append(stit)

    @pyqtSlot(int)
    def kretanje_projektila(self, i):
        if i == 0:
            self.projectile.move(self.projectile.x(), 0)
            self.projectile.setParent(None)
            self.postoji_projectil = False
        else:
            self.projectile.move(self.projectile.x(), self.projectile.y() - 10)

        for i in reversed(self.aliens):
            if i.postoji:
                if (self.projectile.y() >= i.y() and self.projectile.y() <= i.y() + 20) and (
                        self.projectile.x() >= i.x() and self.projectile.x() <= i.x() + 30):
                    i.setParent(None)
                    self.aliens[self.aliens.index(i)].postoji = False
                    self.aliensZaPucanje.remove(i)
                    self.projectile.setParent(None)
                    self.postoji_projectil = False
                    self.skor += 1
                    self.labela_skor.setText("SCORE: " + self.skor.__str__())
                    self.projektil_kretanje.gasenje_signal.emit()
                    break
                if(self.postoji_projectil_vanzemaljaca != False):
                    if(self.projectile.y() >= self.projectile_vanzemaljaca.y() and self.projectile.y() <= self.projectile_vanzemaljaca.y() + 10) and \
                            (self.projectile.x() >= self.projectile_vanzemaljaca.x() and self.projectile.x() <= self.projectile_vanzemaljaca.x() + 10):
                        self.projectile.setParent(None)
                        self.postoji_projectil = False
                        self.projektil_kretanje.gasenje_signal.emit()
                        self.projectile_vanzemaljaca.setParent(None)
                        self.postoji_projectil_vanzemaljaca = False
                        self.projektil_vanzemaljaca_kretanje.gasenje_signal.emit()


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
        projectile.move(alien.x() + 10, alien.y() + 25)
        self.projektil_vanzemaljaca_kretanje = kretanje_projektila_vanzemaljaca_thread(self, self.projectile_vanzemaljaca)
        self.projektil_vanzemaljaca_kretanje.start()

    @pyqtSlot(int)
    def kretanje_projektila_vanzemaljaca(self, i):

        if i == 0:
            self.projectile_vanzemaljaca.move(self.projectile_vanzemaljaca.x(), 800)
            self.projectile_vanzemaljaca.setParent(None)
            self.postoji_projectil_vanzemaljaca = False
        else:
            self.projectile_vanzemaljaca.move(self.projectile_vanzemaljaca.x(), self.projectile_vanzemaljaca.y() + 10)

        if (self.projectile_vanzemaljaca.x() >= self.player.x() and self.projectile_vanzemaljaca.x() <= self.player.x() + 45) and \
                (self.projectile_vanzemaljaca.y() >= self.player.y() and self.projectile_vanzemaljaca.y() <= self.player.y() + 70):
            if self.postoji_projectil_vanzemaljaca:
                for i in self.lista_zivota:
                    if i.postoji:
                        i.setParent(None)
                        self.lista_zivota[self.lista_zivota.index(i)].postoji = False
                        self.lista_preostalih_zivota.remove(i)
                        self.projectile_vanzemaljaca.setParent(None)
                        self.postoji_projectil_vanzemaljaca = False
                        self.projektil_vanzemaljaca_kretanje.gasenje_signal.emit()
                        break
        if (self.postoji_projectil_vanzemaljaca):
            for i in reversed(self.stitovi):
                if (self.projectile_vanzemaljaca.y() >= i.y() and self.projectile_vanzemaljaca.y() <= i.y() + 60) and (
                        self.projectile_vanzemaljaca.x() >= i.x() and self.projectile_vanzemaljaca.x() <= i.x() + 80):
                    if (i.nivo_ostecenja == 0):
                        slika_stita = QPixmap("Ostecenje_1.png")
                        i.setPixmap(slika_stita.scaled(80, 60))
                        i.nivo_ostecenja += 1
                    elif (i.nivo_ostecenja == 1):
                        slika_stita = QPixmap("Ostecenje_2.png")
                        i.setPixmap(slika_stita.scaled(80, 60))
                        i.nivo_ostecenja += 1
                    elif (i.nivo_ostecenja == 2):
                        slika_stita = QPixmap("Ostecenje_3.png")
                        i.setPixmap(slika_stita.scaled(80, 60))
                        i.nivo_ostecenja += 1
                    elif (i.nivo_ostecenja == 3):
                        slika_stita = QPixmap("Ostecenje_4.png")
                        i.setPixmap(slika_stita.scaled(80, 60))
                        i.nivo_ostecenja += 1
                    else:
                        i.setParent(None)
                        self.stitovi.remove(i)
                    self.projektil_vanzemaljaca_kretanje.gasenje_signal.emit()
                    self.projectile_vanzemaljaca.setParent(None)
                    self.postoji_projectil_vanzemaljaca = False
                    break

    def kreiranje_vanzemaljaca(self, vbox):
        slika = "alien2.png"
        red = 1
        kolona = 1
        for i in range(55):
            if i == 0:
                alien = Alien(slika, red, kolona, self)
                vbox.addWidget(alien)
                alien.move(70, 200)
                self.aliens.append(alien)
                self.aliensZaPucanje.append(alien)
            elif i != 0 and i % 11 == 0:
                red += 1
                kolona = 1;
                if red == 2 or red == 3:
                    slika = "alien.png"
                else:
                    slika = "alien3.png"
                alien = Alien(slika, red, kolona, self)
                vbox.addWidget(alien)
                alien.move(self.aliens[i-11].x(), self.aliens[i-11].y() + 40)
                self.aliens.append(alien)
                self.aliensZaPucanje.append(alien)
            else:
                kolona += 1
                alien = Alien(slika, red, kolona, self)
                vbox.addWidget(alien)
                alien.move(self.aliens[i-1].x() + 50, self.aliens[i-1].y())
                self.aliens.append(alien)
                self.aliensZaPucanje.append(alien)



    def kreiranje_zivota(self, vbox):
        zivot = Zivot(self)
        vbox.addWidget(zivot)
        zivot.move(580, 20)
        self.lista_zivota.append(zivot)
        self.lista_preostalih_zivota.append(zivot)

        zivot = Zivot(self)
        vbox.addWidget(zivot)
        zivot.move(620, 20)
        self.lista_zivota.append(zivot)
        self.lista_preostalih_zivota.append(zivot)

        zivot = Zivot(self)
        vbox.addWidget(zivot)
        zivot.move(660, 20)
        self.lista_zivota.append(zivot)
        self.lista_preostalih_zivota.append(zivot)



class kretanje_vanzemaljaca_thread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        kretanje_desno = False
        dosao_do_ivice = False
        nova_iteracija = False
        izvrseno_pomeranje_dole = False

        korak = 11

        while True:
            if nova_iteracija == False:
                time.sleep(1)
            br = 0

            indexVanzemaljca = -1
            pronadjenIndexVanzemaljca = False
            brojProlaza = 0

            while(pronadjenIndexVanzemaljca is False):
                indexProvere = len(self.parent().aliens) - 1

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
                        print(indexProvere)

                brojProlaza += 1

            if nova_iteracija and dosao_do_ivice:
                for i in reversed(self.parent().aliens):
                    self.parent().pomeri_dole_signal.emit(self.parent().aliens.index(i))
                    br += 1
                    if br % 11 == 0:
                        time.sleep(0.05)
            elif kretanje_desno:
                if self.parent().aliens[indexVanzemaljca].x() + 50 <= 650:
                    for i in reversed(self.parent().aliens):
                        self.parent().pomeri_desno_signal.emit(self.parent().aliens.index(i))
                        br += 1
                        if br % 11 == 0:
                            time.sleep(0.05)
                else:
                    kretanje_desno = False
                    dosao_do_ivice = True
            else:
                if self.parent().aliens[indexVanzemaljca].x() - 50 >= 0:
                    for i in reversed(self.parent().aliens):
                        self.parent().pomeri_levo_signal.emit(self.parent().aliens.index(i))
                        br += 1
                        if br % 11 == 0:
                            time.sleep(0.05)
                else:
                    kretanje_desno = True
                    dosao_do_ivice = True

            if dosao_do_ivice and nova_iteracija:
                izvrseno_pomeranje_dole = True

            if dosao_do_ivice and izvrseno_pomeranje_dole == False:
                nova_iteracija = True
            else:
                nova_iteracija = False
                dosao_do_ivice = False
                izvrseno_pomeranje_dole = False

            if(self.parent().postoji_projectil_vanzemaljaca == False):
                self.parent().projektil_vanzemaljaca_kreiranje_signal.emit()



class kretanje_projektila_thread(QThread):

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
            time.sleep(0.03)
            if self.projectile.y() < 100 and self.projectile.y() > 0:
                self.parent().projektil_kretanje_signal.emit(0)
                break
            else:
                self.parent().projektil_kretanje_signal.emit(1)


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
            if self.projectile.y() > 750 and self.projectile.y() < 800:
                self.parent().projektil_vanzemaljaca_kretanje_signal.emit(0)
                break
            else:
                self.parent().projektil_vanzemaljaca_kretanje_signal.emit(1)