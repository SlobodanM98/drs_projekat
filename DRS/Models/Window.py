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

    nova_igra_signal = pyqtSignal(int)
    game_over_signal = pyqtSignal(int)
    sleep_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        ekran = QDesktopWidget().screenGeometry()
        self.razmera_sirina = ekran.width() / 1920
        self.razmera_visina = ekran.height() / 1080

        self.player = Player(self)
        self.aliens = []
        self.aliensZaPucanje = []
        self.lista_zivota = []
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
        self.labela_skor.setFont(QFont('Arial', 13 * self.razmera_sirina))
        self.labela_skor.setText("SCORE: " + self.skor.__str__())
        self.labela_skor.setStyleSheet("color: white; font-weight: bold")
        self.labela_skor.setGeometry(20 * self.razmera_sirina, 30 * self.razmera_visina, 200 * self.razmera_sirina, 20 * self.razmera_visina)

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

        self.setFixedSize(700 * self.razmera_sirina, 800 * self.razmera_visina)
        vbox.addWidget(self.player)
        self.player.move(300 * self.razmera_sirina, 700 * self.razmera_visina)
        self.player.setFocus()

        self.kreiranje_vanzemaljaca()
        self.kreiranje_zivota()

        self.kreiranje_stita()

        self.kretanje_vanzemaljca.start()

        self.setLayout(vbox)
        self.setGeometry(600 * self.razmera_sirina, 100 * self.razmera_sirina, 500 * self.razmera_sirina, 500 * self.razmera_sirina)
        self.setWindowTitle("Space invader")
        self.show()

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

        if self.postoji_projectil:
            self.projektil_kretanje.gasenje_signal.emit()
            self.postoji_projectil = False
            self.projectile.setParent(None)

        if self.postoji_projectil_vanzemaljaca:
            self.projektil_vanzemaljaca_kretanje.gasenje_signal.emit()
            self.postoji_projectil_vanzemaljaca = False
            self.projectile_vanzemaljaca.setParent(None)

        if(novi_nivo == 0):
            self.player.game_over_signal.emit()
            self.labela_game_over.setHidden(False)
            self.labela_klikni_p.setHidden(False)

        if(novi_nivo == 1):
            self.nova_igra_signal.emit(1)

    @pyqtSlot(int)
    def nova_igra(self, novi_nivo):

        if(novi_nivo == 0):
            self.skor = 0
            self.labela_skor.setText("SCORE: " + self.skor.__str__())

        self.player.move(300 * self.razmera_sirina, 700 * self.razmera_visina)

        for i in self.stitovi:
            i.setParent(None)
            self.layout().removeWidget(i)

        self.stitovi.clear()
        self.kreiranje_stita()

        if(novi_nivo == 0):
            self.lista_zivota.clear()
            self.kreiranje_zivota()

        for i in self.aliens:
            i.setParent(None)
            self.layout().removeWidget(i)

        self.aliensZaPucanje.clear()
        self.aliens.clear()
        self.kreiranje_vanzemaljaca()

        if (novi_nivo == 1):
            self.labela_game_over.setText("NOVI NIVO")
            self.labela_game_over.setHidden(False)
            self.spavanje = sleep_thread(self)
            self.spavanje.start()

        if novi_nivo == 0:
            self.labela_game_over.setHidden(True)
            self.labela_klikni_p.setHidden(True)

            self.kretanje_vanzemaljca = kretanje_vanzemaljaca_thread(self)
            self.kretanje_vanzemaljca.start()


    @pyqtSlot(int)
    def pomeranje_dole(self, i):
        self.aliens[i].move(self.aliens[i].x(), self.aliens[i].y() + 20 * self.razmera_visina)

    @pyqtSlot(int)
    def pomeranje_desno(self, i):
        self.aliens[i].move(self.aliens[i].x() + 15 * self.razmera_sirina, self.aliens[i].y())

    @pyqtSlot(int)
    def pomeranje_levo(self, i):
        self.aliens[i].move(self.aliens[i].x() - 15 * self.razmera_sirina, self.aliens[i].y())

    @pyqtSlot(int)
    def pomeranje_igraca(self, i):
        if i == 0:
            self.player.move(self.player.x() + 10 * self.razmera_sirina, self.player.y())
        else:
            self.player.move(self.player.x() - 10 * self.razmera_sirina, self.player.y())

    @pyqtSlot()
    def kreiranje_projektila(self):
        projectile = Projectile(self)
        self.projectile = projectile
        self.postoji_projectil = True
        self.layout().addWidget(self.projectile)
        projectile.move(self.player.x() + 21 * self.razmera_sirina, self.player.y() - 5 * self.razmera_visina)
        self.projektil_kretanje = kretanje_projektila_thread(self, self.projectile)
        self.projektil_kretanje.start()

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

    @pyqtSlot(int)
    def kretanje_projektila(self, i):
        if i == 0:
            self.projectile.move(self.projectile.x(), 0)
            self.projectile.setParent(None)
            self.postoji_projectil = False
        else:
            self.projectile.move(self.projectile.x(), self.projectile.y() - 20 * self.razmera_visina)

        if self.postoji_projectil:
            for i in reversed(self.aliens):
                if i.postoji:
                    if (self.projectile.y() >= i.y() and self.projectile.y() <= i.y() + 20 * self.razmera_visina) and (
                            self.projectile.x() >= i.x() and self.projectile.x() <= i.x() + 30 * self.razmera_visina):
                        self.aliens[self.aliens.index(i)].postoji = False
                        i.setParent(None)
                        self.aliensZaPucanje.remove(i)
                        self.projectile.setParent(None)
                        self.postoji_projectil = False
                        self.skor += 1
                        self.labela_skor.setText("SCORE: " + self.skor.__str__())
                        self.projektil_kretanje.gasenje_signal.emit()
                        break
        if len(self.aliensZaPucanje) == 0:
            self.game_over_signal.emit(1)
        if(self.postoji_projectil_vanzemaljaca != False):
            if(self.projectile.y() >= self.projectile_vanzemaljaca.y() and self.projectile.y() <= self.projectile_vanzemaljaca.y() + 10 * self.razmera_visina) and \
                            (self.projectile.x() >= self.projectile_vanzemaljaca.x() and self.projectile.x() <= self.projectile_vanzemaljaca.x() + 10 * self.razmera_visina):
                self.projectile.setParent(None)
                self.postoji_projectil = False
                self.projektil_kretanje.gasenje_signal.emit()
                self.projectile_vanzemaljaca.setParent(None)
                self.postoji_projectil_vanzemaljaca = False
                self.projektil_vanzemaljaca_kretanje.gasenje_signal.emit()

        if (self.postoji_projectil):
            for i in self.stitovi:
                if (self.projectile.y() >= i.y() and self.projectile.y() <= i.y() + 50 * self.razmera_visina) and (
                        self.projectile.x() >= i.x() and self.projectile.x() <= i.x() + 70 * self.razmera_visina):
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
                    self.projektil_kretanje.gasenje_signal.emit()
                    self.projectile.setParent(None)
                    self.postoji_projectil = False
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

        if (self.projectile_vanzemaljaca.x() >= self.player.x() and self.projectile_vanzemaljaca.x() <= self.player.x() + 45 * self.razmera_visina) and \
                (self.projectile_vanzemaljaca.y() >= self.player.y() and self.projectile_vanzemaljaca.y() <= self.player.y() + 70 * self.razmera_visina):
            if self.postoji_projectil_vanzemaljaca:
                for i in self.lista_zivota:
                    if i.postoji:
                        i.setParent(None)
                        self.lista_zivota[self.lista_zivota.index(i)].postoji = False
                        self.lista_zivota.remove(i)
                        self.projectile_vanzemaljaca.setParent(None)
                        self.postoji_projectil_vanzemaljaca = False
                        self.projektil_vanzemaljaca_kretanje.gasenje_signal.emit()
                        break

                if len(self.lista_zivota) == 0:
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
        zivot.move(580 * self.razmera_sirina, 20 * self.razmera_visina)
        self.lista_zivota.append(zivot)

        zivot = Zivot(self)
        self.layout().addWidget(zivot)
        zivot.move(620 * self.razmera_sirina, 20 * self.razmera_visina)
        self.lista_zivota.append(zivot)

        zivot = Zivot(self)
        self.layout().addWidget(zivot)
        zivot.move(660 * self.razmera_sirina, 20 * self.razmera_visina)
        self.lista_zivota.append(zivot)

class sleep_thread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        time.sleep(2)
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

        korak = 11

        spavanje_niti = 1
        broj_zivih = len(self.parent().aliensZaPucanje)
        vreme_za_pucanje = 0
        granica_za_pucanje = 1

        while self.gasenje is False:
            if broj_zivih <= 44 and broj_zivih > 34:
                spavanje_niti = 0.8
            elif broj_zivih <= 33 and broj_zivih > 23:
                spavanje_niti = 0.6
            elif broj_zivih <= 22 and broj_zivih > 12:
                spavanje_niti = 0.5
            elif broj_zivih <= 11 and broj_zivih > 6:
                granica_za_pucanje = 0.6
                spavanje_niti = 0.3
            elif broj_zivih <= 5 and broj_zivih > 3:
                granica_za_pucanje = 0.4
                spavanje_niti = 0.2
            elif broj_zivih == 2:
                spavanje_niti = 0.1
            elif broj_zivih == 1:
                granica_za_pucanje = 0.5
                spavanje_niti = 0.5

            if nova_iteracija == False:
                time.sleep(spavanje_niti)
                vreme_za_pucanje += spavanje_niti
            br = 0

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

            if dosao_do_ivice and izvrseno_pomeranje_dole == False:
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
                if self.parent().postoji_projectil_vanzemaljaca == False:
                    self.parent().projektil_vanzemaljaca_kreiranje_signal.emit()
                    vreme_za_pucanje = 0

            broj_zivih = len(self.parent().aliensZaPucanje)



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
            if self.projectile.y() < 100 * self.parent().razmera_visina and self.projectile.y() > 0:
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
            if self.projectile.y() > 750 * self.parent().razmera_visina and self.projectile.y() < 800 * self.parent().razmera_visina:
                self.parent().projektil_vanzemaljaca_kretanje_signal.emit(0)
                break
            else:
                self.parent().projektil_vanzemaljaca_kretanje_signal.emit(1)