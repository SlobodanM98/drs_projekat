import time
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDesktopWidget, QLabel, QWidget, \
    QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
from Models.Player import Player
from Models.Projectile import Projectile
from Models.Alien import Alien


class Window(QMainWindow):

    pomeri_dole_signal = pyqtSignal(int)
    pomeri_desno_signal = pyqtSignal(int)
    pomeri_levo_signal = pyqtSignal(int)

    player_kretanje_signal = pyqtSignal(int)
    projektil_kreiranje_signal = pyqtSignal()
    projektil_kretanje_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.player = Player(self)
        self.aliens = []
        self.projectile = None
        self.postoji_projectil = False

        self.set_ui()

    def set_ui(self):
        self.setStyleSheet("background-color: black;")
        vbox = QVBoxLayout(self)

        self.pomeri_dole_signal.connect(self.pomeranje_dole)
        self.pomeri_desno_signal.connect(self.pomeranje_desno)
        self.pomeri_levo_signal.connect(self.pomeranje_levo)

        self.player_kretanje_signal.connect(self.pomeranje_igraca)
        self.projektil_kreiranje_signal.connect(self.kreiranje_projektila)
        self.projektil_kretanje_signal.connect(self.kretanje_projektila)

        self.kretanje_vanzemaljca = kretanje_vanzemaljaca_thread(self)

        self.setFixedSize(700, 800)
        vbox.addWidget(self.player)
        self.player.move(300, 700)
        self.player.setFocus()

        self.kreiranje_vanzemaljaca(vbox)

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
            self.player.move(self.player.x() + 5, self.player.y())
        else:
            self.player.move(self.player.x() - 5, self.player.y())

    @pyqtSlot()
    def kreiranje_projektila(self):
        projectile = Projectile(self)
        self.projectile = projectile
        self.postoji_projectil = True
        self.layout().addWidget(self.projectile)
        projectile.move(self.player.x() + 38.5, self.player.y() - 5)
        self.projektil_kretanje = kretanje_projektila_thread(self, self.projectile)
        self.projektil_kretanje.start()

    @pyqtSlot(int)
    def kretanje_projektila(self, i):
        if i == 0:
            self.projectile.move(self.projectile.x(), 0)
            self.projectile.setParent(None)
            self.postoji_projectil = False
        else:
            self.projectile.move(self.projectile.x(), self.projectile.y() - 16)

        for i in reversed(self.aliens):
            if (self.projectile.y() >= i.y() and self.projectile.y() <= i.y() + 20) and (
                    self.projectile.x() >= i.x() and self.projectile.x() <= i.x() + 30):
                i.setParent(None)
                self.aliens.remove(i)
                self.projectile.setParent(None)
                self.postoji_projectil = False
                self.projektil_kretanje.gasenje_signal.emit()
                break


    def kreiranje_vanzemaljaca(self, vbox):
        slika = "alien2.png"
        line = 1
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


class kretanje_vanzemaljaca_thread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        kretanje_desno = False
        dosao_do_ivice = False
        nova_iteracija = False
        izvrseno_pomeranje_dole = False
        while True:
            if nova_iteracija == False:
                time.sleep(1)
            br = 0
            if nova_iteracija and dosao_do_ivice:
                for i in reversed(self.parent().aliens):
                    self.parent().pomeri_dole_signal.emit(self.parent().aliens.index(i))
                    br += 1
                    if br % 11 == 0:
                        time.sleep(0.05)
            elif kretanje_desno:
                for i in reversed(self.parent().aliens):
                    if br == 0:
                        if i.x() + 80 <= 700:
                            self.parent().pomeri_desno_signal.emit(self.parent().aliens.index(i))
                            br += 1
                        else:
                            kretanje_desno = False
                            dosao_do_ivice = True
                            break
                    else:
                        self.parent().pomeri_desno_signal.emit(self.parent().aliens.index(i))
                        br += 1
                    if br % 11 == 0:
                        time.sleep(0.05)
            else:
                for i in reversed(self.parent().aliens):
                    if br == 0:
                        if i.x() - 550 >= 0:
                            self.parent().pomeri_levo_signal.emit(self.parent().aliens.index(i))
                            br += 1
                        else:
                            kretanje_desno = True
                            dosao_do_ivice = True
                            break
                    else:
                        self.parent().pomeri_levo_signal.emit(self.parent().aliens.index(i))
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
            time.sleep(0.05)
            if self.projectile.y() < 100 and self.projectile.y() > 0:
                self.parent().projektil_kretanje_signal.emit(0)
                break
            else:
                self.parent().projektil_kretanje_signal.emit(1)