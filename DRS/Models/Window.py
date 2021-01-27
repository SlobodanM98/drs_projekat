import random
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from Models.Player import Player
from Models.Projectile import Projectile
from Models.Alien import Alien
from Models.Health import Zivot
from Models.Stit import Stit
from Threads.Sila_thread import sila_thread
from Threads.Sleep_thread import sleep_thread
from Threads.Kretanje_vanzemaljaca_thread import kretanje_vanzemaljaca_thread
from Threads.Kretanje_projektila_thread import kretanje_projektila_thread
from Threads.Kretanje_projektila_vanzemaljaca_thread import kretanje_projektila_vanzemaljaca_thread


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

    nova_runda_signal = pyqtSignal()
    sila_signal = pyqtSignal(list)
    prikaz_sile_signal = pyqtSignal(int)

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
        self.projectiles[0].setHidden(True)
        self.projectiles[1].setHidden(True)
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
        self.score_igraca = []
        self.plasirani_igraci = []
        self.turnir = False
        self.cetiri_igraca = False
        self.runda = -1
        self.nivo = 0

        self.pocetni_prozor()

    def pocetni_prozor(self):
        self.dugme_jedan_igrac = QPushButton('Jedan igrac', self)
        self.dugme_jedan_igrac.setStyleSheet('''QPushButton {color: white; border: 1px solid; border-color: white}QPushButton:hover {background-color: #328930;}''')
        self.dugme_jedan_igrac.setGeometry(280 * self.razmera_sirina, 200 * self.razmera_visina, 150 * self.razmera_sirina, 50 * self.razmera_visina)
        self.dugme_jedan_igrac.setFont(QFont('Ariel', 12))
        self.dugme_jedan_igrac.clicked.connect(self.jedan_igrac)
        self.dugme_jedan_igrac.setHidden(False)

        self.dugme_dva_igraca = QPushButton('Dva igraca', self)
        self.dugme_dva_igraca.setStyleSheet('''QPushButton {color: white; border: 1px solid; border-color: white}QPushButton:hover {background-color: #328930;}''')
        self.dugme_dva_igraca.setGeometry(280 * self.razmera_sirina, 300 * self.razmera_visina, 150 * self.razmera_sirina, 50 * self.razmera_visina)
        self.dugme_dva_igraca.setFont(QFont('Ariel', 12))
        self.dugme_dva_igraca.clicked.connect(self.dva_igraca)
        self.dugme_dva_igraca.setHidden(False)

        self.dugme_turnir_4 = QPushButton('Turnir (4)', self)
        self.dugme_turnir_4.setStyleSheet('''QPushButton {color: white; border: 1px solid; border-color: white}QPushButton:hover {background-color: #328930;}''')
        self.dugme_turnir_4.setGeometry(180 * self.razmera_sirina, 400 * self.razmera_visina, 150 * self.razmera_sirina, 50 * self.razmera_visina)
        self.dugme_turnir_4.setFont(QFont('Ariel', 12))
        self.dugme_turnir_4.clicked.connect(self.turnir_4)
        self.dugme_turnir_4.setHidden(False)

        self.dugme_turnir_8 = QPushButton('Turnir (8)', self)
        self.dugme_turnir_8.setStyleSheet('''QPushButton {color: white; border: 1px solid; border-color: white}QPushButton:hover {background-color: #328930;}''')
        self.dugme_turnir_8.setGeometry(380 * self.razmera_sirina, 400 * self.razmera_visina, 150 * self.razmera_sirina, 50 * self.razmera_visina)
        self.dugme_turnir_8.setFont(QFont('Ariel', 12))
        self.dugme_turnir_8.clicked.connect(self.turnir_8)
        self.dugme_turnir_8.setHidden(False)

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

    def turnir_4(self):
        self.turnir = True
        self.cetiri_igraca = True
        self.runda = 1
        self.dva_igraca()

    def turnir_8(self):
        self.turnir = True
        self.cetiri_igraca = False
        self.runda = 1
        self.dva_igraca()

    def jedan_igrac(self):
        self.nova_igra_signal.emit([0, 0])

        self.dugme_jedan_igrac.setHidden(True)
        self.dugme_dva_igraca.setHidden(True)
        self.dugme_turnir_4.setHidden(True)
        self.dugme_turnir_8.setHidden(True)
        self.dugme_izadji.setHidden(True)

        if self.ucitan_ui is False:
            self.players.append(Player(self))
            self.players.append(Player(self))
            self.players[0].dva_igraca = False
            self.players[1].dva_igraca = False
            self.set_ui()
            self.labela_skor2.setHidden(True)
            self.labela_igrac2.setHidden(True)
            self.ucitan_ui = True
        else:
            self.labela_game_over.setHidden(True)
            self.labela_klikni_p.setHidden(True)
            self.labela_skor.setHidden(False)
            self.labela_skor2.setHidden(True)
            self.labela_igrac1.setHidden(False)
            self.labela_igrac2.setHidden(True)
            self.players[0].setHidden(False)
            self.players[1].setHidden(True)
            self.players[0].dva_igraca = False
            self.players[1].dva_igraca = False
            self.labela_skor.setHidden(False)
            self.players[0].game_on_signal.emit()
            self.players[0].setFocus()
            self.kretanje_vanzemaljca = kretanje_vanzemaljaca_thread(self)
            self.kretanje_vanzemaljca.start()
            self.delovanje_sile = sila_thread(self)
            self.delovanje_sile.start()

    def dva_igraca(self):
        self.nova_igra_signal.emit([0, 1])

        self.dugme_jedan_igrac.setHidden(True)
        self.dugme_dva_igraca.setHidden(True)
        self.dugme_turnir_4.setHidden(True)
        self.dugme_turnir_8.setHidden(True)
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
            self.labela_igrac1.setHidden(False)
            self.labela_igrac2.setHidden(False)

            self.players[0].setHidden(False)
            self.players[1].setHidden(False)
            self.players[0].dva_igraca = True
            self.players[1].dva_igraca = True
            self.players[0].game_on_signal.emit()
            self.players[1].game_on_signal.emit()
            self.players[0].setFocus()
            self.kretanje_vanzemaljca = kretanje_vanzemaljaca_thread(self)
            self.kretanje_vanzemaljca.start()
            self.delovanje_sile = sila_thread(self)
            self.delovanje_sile.start()

        self.labela_game_over.setText("GAME OVER")
        self.labela_game_over.setGeometry(300 * self.razmera_sirina, 30 * self.razmera_visina, 200 * self.razmera_sirina, 20 * self.razmera_visina)

        if self.turnir:
            if self.cetiri_igraca:
                if self.runda == 3:
                    if self.score_igraca[0] > self.score_igraca[1]:
                        self.labela_igrac1.setText("Player 1")
                    else:
                        self.labela_igrac1.setText("Player 2")

                    if self.score_igraca[2] > self.score_igraca[3]:
                        self.labela_igrac2.setText("Player 3")
                    else:
                        self.labela_igrac2.setText("Player 4")
                else:
                    self.labela_igrac1.setText("Player " + str(self.runda * 2 - 1))
                    self.labela_igrac2.setText("Player " + str(self.runda * 2))
            else:
                if self.runda == 5:
                    if self.score_igraca[0] > self.score_igraca[1]:
                        self.labela_igrac1.setText("Player 1")
                        self.plasirani_igraci.append(1)
                    else:
                        self.labela_igrac1.setText("Player 2")
                        self.plasirani_igraci.append(2)

                    if self.score_igraca[2] > self.score_igraca[3]:
                        self.labela_igrac2.setText("Player 3")
                        self.plasirani_igraci.append(3)
                    else:
                        self.labela_igrac2.setText("Player 4")
                        self.plasirani_igraci.append(4)
                elif self.runda == 6:
                    if self.score_igraca[4] > self.score_igraca[5]:
                        self.labela_igrac1.setText("Player 5")
                        self.plasirani_igraci.append(5)
                    else:
                        self.labela_igrac1.setText("Player 6")
                        self.plasirani_igraci.append(6)

                    if self.score_igraca[6] > self.score_igraca[7]:
                        self.labela_igrac2.setText("Player 7")
                        self.plasirani_igraci.append(7)
                    else:
                        self.labela_igrac2.setText("Player 8")
                        self.plasirani_igraci.append(8)
                elif self.runda == 7:
                    if self.score_igraca[8] > self.score_igraca[9]:
                        self.labela_igrac1.setText("Player " + str(self.plasirani_igraci[0]))
                    else:
                        self.labela_igrac1.setText("Player " + str(self.plasirani_igraci[1]))

                    if self.score_igraca[10] > self.score_igraca[11]:
                        self.labela_igrac2.setText("Player " + str(self.plasirani_igraci[2]))
                    else:
                        self.labela_igrac2.setText("Player " + str(self.plasirani_igraci[3]))
                else:
                    self.labela_igrac1.setText("Player " + str(self.runda * 2 - 1))
                    self.labela_igrac2.setText("Player " + str(self.runda * 2))
        else:
            self.labela_igrac1.setText("Player 1")
            self.labela_igrac2.setText("Player 2")
            self.labela_game_over.setText("GAME OVER")
            self.labela_game_over.setGeometry(300 * self.razmera_sirina, 30 * self.razmera_visina, 200 * self.razmera_sirina, 20 * self.razmera_visina)

    def set_ui(self):
        self.labela_igrac1 = QLabel(self)
        self.labela_igrac1.setFont(QFont('Arial', 13 * self.razmera_sirina))
        self.labela_igrac1.setText("Player 1")
        self.labela_igrac1.setStyleSheet("color: white; font-weight: bold")
        self.labela_igrac1.setGeometry(20 * self.razmera_sirina, 30 * self.razmera_visina, 200 * self.razmera_sirina, 20 * self.razmera_visina)
        self.labela_igrac1.setHidden(False)

        self.labela_igrac2 = QLabel(self)
        self.labela_igrac2.setFont(QFont('Arial', 13 * self.razmera_sirina))
        self.labela_igrac2.setText("Player 2")
        self.labela_igrac2.setStyleSheet("color: white; font-weight: bold")
        self.labela_igrac2.setGeometry(580 * self.razmera_sirina, 30 * self.razmera_visina, 200 * self.razmera_sirina, 20 * self.razmera_visina)
        self.labela_igrac2.setHidden(False)

        self.labela_skor = QLabel(self)
        self.labela_skor.setFont(QFont('Arial', 13 * self.razmera_sirina))
        self.labela_skor.setText("SCORE: " + self.skor.__str__())
        self.labela_skor.setStyleSheet("color: white; font-weight: bold")
        self.labela_skor.setGeometry(20 * self.razmera_sirina, 60 * self.razmera_visina, 200 * self.razmera_sirina, 20 * self.razmera_visina)
        self.labela_skor.setHidden(False)

        self.labela_skor2 = QLabel(self)
        self.labela_skor2.setFont(QFont('Arial', 13 * self.razmera_sirina))
        self.labela_skor2.setText("SCORE: " + self.skor.__str__())
        self.labela_skor2.setStyleSheet("color: white; font-weight: bold")
        self.labela_skor2.setGeometry(580 * self.razmera_sirina, 60 * self.razmera_visina, 200 * self.razmera_sirina, 20 * self.razmera_visina)
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

        self.labela_grom = QLabel(self)
        slika = QPixmap("grom.png")
        self.labela_grom.setPixmap(slika.scaled(15 * self.razmera_sirina, 20 * self.razmera_visina))
        self.labela_grom.resize(15 * self.razmera_sirina, 20 * self.razmera_visina)
        self.layout().addWidget(self.labela_grom)
        self.labela_grom.move(320 * self.razmera_sirina, 670 * self.razmera_visina)
        self.labela_grom.setHidden(True)


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

        self.nova_runda_signal.connect(self.nova_runda)
        self.sila_signal.connect(self.sila)
        self.prikaz_sile_signal.connect(self.prikaz_sile)

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

        self.delovanje_sile = sila_thread(self)
        self.delovanje_sile.start()

    @pyqtSlot(int)
    def prikaz_sile(self, prikazi):
        if prikazi == 0:
            self.labela_grom.setHidden(True)
        elif prikazi == 1:
            self.labela_grom.setHidden(False)

    def nova_runda(self):
        self.dva_igraca()

    def closeEvent(self, event):
        if self.ucitan_ui is True:
            self.players[0].game_over_signal.emit(0)
            self.players[0].game_over_signal.emit(1)
            self.kretanje_vanzemaljca.gasenje_signal.emit()
            self.kretanje_vanzemaljca.wait(1000)
            self.kretanje_vanzemaljca.terminate()

            self.delovanje_sile.gasenje_signal.emit()
            self.delovanje_sile.wait(1000)
            self.delovanje_sile.terminate()

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

    @pyqtSlot(list)   #params[0] - dobra(0) ili losa(1) sila, params[1] - prvi(0) ili drugi(1) igrac
    def sila(self, params):
        if params[0] == 0:
            if params[1] == 0:
                brSrca = 0
                for i in self.lista_zivota:
                    if i.postoji is True:
                        brSrca += 1
                if brSrca == 1:
                    self.lista_zivota[1].postoji = True
                    self.lista_zivota[1].setHidden(False)
                elif brSrca == 2:
                    self.lista_zivota[0].postoji = True
                    self.lista_zivota[0].setHidden(False)
            elif params[1] == 1:
                brSrca = 0
                for i in self.lista_zivota2:
                    if i.postoji is True:
                        brSrca += 1

                if brSrca == 1:
                    self.lista_zivota2[1].postoji = True
                    self.lista_zivota2[1].setHidden(False)
                elif brSrca == 2:


                    self.lista_zivota2[0].postoji = True
                    self.lista_zivota2[0].setHidden(False)
        elif params[0] == 1:
            if self.postoji_projectil_vanzemaljaca and self.projectile_vanzemaljaca.y() < 700:
                self.players[params[1]].move(self.projectile_vanzemaljaca.x() - 15 * self.razmera_sirina, self.players[params[1]].y())

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

        self.labela_grom.setHidden(True)
        self.labela_game_over.setHidden(True)
        self.labela_klikni_p.setHidden(True)
        self.labela_skor.setHidden(True)
        self.labela_skor2.setHidden(True)
        self.labela_igrac1.setHidden(True)
        self.labela_igrac2.setHidden(True)

        self.players[0].setHidden(True)
        self.players[1].setHidden(True)

        self.dugme_jedan_igrac.setHidden(False)
        self.dugme_dva_igraca.setHidden(False)
        self.dugme_turnir_4.setHidden(False)
        self.dugme_turnir_8.setHidden(False)
        self.dugme_izadji.setHidden(False)

    @pyqtSlot()
    def sleepp(self):
        self.labela_game_over.setHidden(True)
        self.labela_game_over.setText("GAME OVER")
        self.labela_klikni_p.setHidden(True)

        self.kretanje_vanzemaljca = kretanje_vanzemaljaca_thread(self)
        self.kretanje_vanzemaljca.start()

        self.delovanje_sile = sila_thread(self)
        self.delovanje_sile.start()

    @pyqtSlot(int)   # 0 - game over, 1 - novi nivo
    def game_over(self, novi_nivo):
        self.kretanje_vanzemaljca.gasenje_signal.emit()
        self.delovanje_sile.gasenje_signal.emit()

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
            if self.turnir:
                self.runda += 1
                if self.skor == self.skor2:
                    x = random.randint(0, 1)
                    if x == 0:
                        self.skor += 1
                    else:
                        self.skor2 += 1
                self.score_igraca.append(self.skor)
                self.score_igraca.append(self.skor2)
                if self.cetiri_igraca:
                    if self.runda == 4:
                        self.turnir = False
                        self.runda = -1
                        self.cetiri_igraca = False
                        self.score_igraca = []
                elif self.runda == 8:
                    self.turnir = False
                    self.runda = -1
                    self.cetiri_igraca = False
                    self.score_igraca = []
                    self.plasirani_igraci = []

                if self.skor > self.skor2:
                    self.labela_game_over.setText("Pobednik je " + self.labela_igrac1.text())
                else:
                    self.labela_game_over.setText("Pobednik je " + self.labela_igrac2.text())
                self.labela_game_over.setGeometry(250 * self.razmera_sirina, 30 * self.razmera_visina, 250 * self.razmera_sirina, 20 * self.razmera_visina)

            self.players[0].game_over_signal.emit(0)
            self.labela_game_over.setHidden(False)
            self.labela_klikni_p.setHidden(True)
            self.nivo = 0
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
            self.nivo += 1
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
        if self.postoji_projectils[index] is False:
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
        stit.move(225 * self.razmera_sirina, 600 * self.razmera_visina)
        self.stitovi.append(stit)
        stit = Stit(self)
        self.layout().addWidget(stit)
        stit.move(395 * self.razmera_sirina, 600 * self.razmera_visina)
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
        if self.postoji_projectil_vanzemaljaca is False:
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
                                i.setHidden(True)
                                self.lista_zivota[self.lista_zivota.index(i)].postoji = False
                                #self.lista_zivota.remove(i)
                                self.projectile_vanzemaljaca.setParent(None)
                                brSrca = 0
                                for i in self.lista_zivota:
                                    if i.postoji is True:
                                        brSrca += 1
                                if(brSrca == 0):
                                    self.players[index].game_over_signal.emit(0)
                                    self.players[index].setHidden(True)
                                self.postoji_projectil_vanzemaljaca = False
                                self.projektil_vanzemaljaca_kretanje.gasenje_signal.emit()
                                break
                    elif index == 1:
                        for i in self.lista_zivota2:
                            if i.postoji:
                                i.setHidden(True)
                                self.lista_zivota2[self.lista_zivota2.index(i)].postoji = False
                                #self.lista_zivota2.remove(i)
                                brSrca = 0
                                for i in self.lista_zivota2:
                                    if i.postoji is True:
                                        brSrca += 1
                                if (brSrca == 0):
                                    self.players[0].game_over_signal.emit(1)
                                    self.players[index].setHidden(True)
                                self.projectile_vanzemaljaca.setParent(None)
                                self.postoji_projectil_vanzemaljaca = False
                                self.projektil_vanzemaljaca_kretanje.gasenje_signal.emit()
                                break

                    if self.players[0].dva_igraca is False:
                        brSrca = 0
                        for i in self.lista_zivota:
                            if i.postoji is True:
                                brSrca += 1
                        if brSrca == 0:
                            self.game_over_signal.emit(0)
                    else:
                        brSrca = 0
                        for i in self.lista_zivota:
                            if i.postoji is True:
                                brSrca += 1
                        for i in self.lista_zivota2:
                            if i.postoji is True:
                                brSrca += 1
                        if brSrca == 0:
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
        zivot.move(20 * self.razmera_sirina, 90 * self.razmera_visina)
        self.lista_zivota.append(zivot)

        zivot = Zivot(self)
        self.layout().addWidget(zivot)
        zivot.move(60 * self.razmera_sirina, 90 * self.razmera_visina)
        self.lista_zivota.append(zivot)

        zivot = Zivot(self)
        self.layout().addWidget(zivot)
        zivot.move(100 * self.razmera_sirina, 90 * self.razmera_visina)
        self.lista_zivota.append(zivot)

    def kreiranje_zivota2(self):
        zivot = Zivot(self)
        self.layout().addWidget(zivot)
        zivot.move(580 * self.razmera_sirina, 90 * self.razmera_visina)
        self.lista_zivota2.append(zivot)

        zivot = Zivot(self)
        self.layout().addWidget(zivot)
        zivot.move(620 * self.razmera_sirina, 90 * self.razmera_visina)
        self.lista_zivota2.append(zivot)

        zivot = Zivot(self)
        self.layout().addWidget(zivot)
        zivot.move(660 * self.razmera_sirina, 90 * self.razmera_visina)
        self.lista_zivota2.append(zivot)