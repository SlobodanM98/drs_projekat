import time
from threading import Thread

from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDesktopWidget, QLabel, QWidget, \
    QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap
import sys
from Models.Player import Player
from Models.Projectile import Projectile
from Models.Alien import Alien


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.player = Player(self)
        self.aliens = []

        self.set_ui()

    def set_ui(self):
        self.setStyleSheet("background-color: black;")
        vbox = QVBoxLayout(self)

        self.player.projektil_signal.connect(self.kreiranje_projektila)

        self.setFixedSize(700, 800)
        vbox.addWidget(self.player)
        self.player.move(300, 700)
        self.player.setFocus()

        self.kreiranje_vanzemaljaca(vbox)
        kretanje_aliena_tred = Thread(target=self.kretanje_aliena, args=[])
        kretanje_aliena_tred.start()
        self.setLayout(vbox)
        self.setGeometry(600, 100, 500, 500)
        self.setWindowTitle("Space invader")
        self.show()

    @pyqtSlot()
    def kreiranje_projektila(self):
        projectile = Projectile(self)
        self.layout().addWidget(projectile)
        projectile.move(self.player.x() + 38.5, self.player.y() - 5)
        nit = Thread(target=self.kretanje_projektila, args=[projectile])
        nit.start()

    def kretanje_projektila(self, projectile):
        izlaz = False
        while projectile.y() > 0 and izlaz == False:
            time.sleep(0.03)
            if projectile.y() < 100 and projectile.y() > 0:
                projectile.move(projectile.x(), 0)
            else:
                projectile.move(projectile.x(), projectile.y() - 16)
        projectile.setParent(None)


    def kreiranje_vanzemaljaca(self, vbox):
        slika = "alien2.png"
        line = 1;
        for i in range(55):
            if i == 0:
                alien = Alien(slika, self)
                vbox.addWidget(alien)
                alien.move(70, 200)
                self.aliens.append(alien)
            elif i != 0 and i % 11 == 0:
                line += 1
                if line == 2 or line == 3:
                    slika = "alien.png"
                else:
                    slika = "alien3.png"
                alien = Alien(slika, self)
                vbox.addWidget(alien)
                alien.move(self.aliens[i-11].x(), self.aliens[i-11].y() + 40)
                self.aliens.append(alien)
            else:
                alien = Alien(slika, self)
                vbox.addWidget(alien)
                alien.move(self.aliens[i-1].x() + 50, self.aliens[i-1].y())
                self.aliens.append(alien)

    def kretanje_aliena(self):
        kretanje_desno = False
        dosao_do_ivice = False
        nova_iteracija = False
        izvrseno_pomeranje_dole = False
        while True:
            if nova_iteracija == False:
                time.sleep(1)
            br = 0
            if nova_iteracija and dosao_do_ivice:
                for i in reversed(self.aliens):
                    i.move(i.x(), i.y() + 20)
                    br += 1
                    if br % 11 == 0:
                        time.sleep(0.05)
            elif kretanje_desno:
                for i in reversed(self.aliens):
                    if br == 0:
                        if i.x() + 80 <= 700:
                            i.move(i.x() + 10, i.y())
                            br += 1
                        else:
                            kretanje_desno = False
                            dosao_do_ivice = True
                            break
                    else:
                        i.move(i.x() + 10, i.y())
                        br += 1
                    if br % 11 == 0:
                        time.sleep(0.05)
            else:
                for i in reversed(self.aliens):
                    if br == 0:
                        if i.x() - 550 >= 0:
                            i.move(i.x() - 10, i.y())
                            br += 1
                        else:
                            kretanje_desno = True
                            dosao_do_ivice = True
                            break
                    else:
                        i.move(i.x() - 10, i.y())
                        br += 1
                    if br % 11 == 0:
                        time.sleep(0.05)

            if dosao_do_ivice and nova_iteracija:
                izvrseno_pomeranje_dole = True

            if dosao_do_ivice and izvrseno_pomeranje_dole == False:
                nova_iteracija = True
            else:
                nova_iteracija = False
                dosao_do_ivice = False
                izvrseno_pomeranje_dole = False

