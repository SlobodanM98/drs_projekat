from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
import random
import time

class sila_thread(QThread):
    gasenje_signal = pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent)
        self.deluje_od = 250 * self.parent().razmera_sirina
        self.deluje_do = 350 * self.parent().razmera_sirina
        self.gasenje = False
        self.gasenje_signal.connect(self.izlaz)

    @pyqtSlot()
    def izlaz(self):
        self.gasenje = True

    def run(self):
        while self.gasenje is False:
            time.sleep(1.8)
            self.parent().prikaz_sile_signal.emit(1)
            time.sleep(0.2)
            sila = random.randint(1, 10)
            prvi = False
            drugi = False
            if (self.parent().players[0].x() >= self.deluje_od and self.parent().players[0].x() <= self.deluje_do):
                prvi = True
            if(self.parent().players[0].dva_igraca is True):
                if (self.parent().players[1].x() >= self.deluje_od and self.parent().players[1].x() <= self.deluje_do):
                    drugi = True
            x = -1
            if prvi is True and drugi is True:
                x = random.randint(0, 1)
            elif prvi is True:
                x = 0
            elif drugi is True:
                x = 1
            if x != -1:
                if sila >= 8:
                    self.parent().sila_signal.emit([0, x])
                else:
                    self.parent().sila_signal.emit([1, x])
            self.parent().prikaz_sile_signal.emit(0)